import os
import requests
import json
import time
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseNotFound
import urllib.request


media_location = settings.MEDIA_ROOT

class ProjectHandler(View):
    def get(self, *args, **kwargs):
        projects = Project.objects.filter(user=self.request.user).order_by('-created_at')

            
        context = {
            'projects':projects,
        }
        return render(self.request, 'start-app.html', context)
    
    def post(self, *args, **kwargs):
        # Get the project name from the POST request
        project_name = self.request.POST.get('name')
        # Create a new project
        project, project_created = Project.objects.get_or_create(user=self.request.user, name=project_name)
        if project_created == False:
            print("already there")
        project_properties, project_properties_created = ProjectProperties.objects.get_or_create(project=project)
        if project_properties_created == False:
            print("already there")
        # Return the project information as JSON
        response_data = {'name': project.name}

        return redirect('core:projects')

class SelectAvatars(View):
    def get(self, *args, **kwargs):
        slug = kwargs['slug']
        print(slug)
        print(self.request)
        context = {
            # \
        }
        return render(self.request, 'select-avatar.html', context)
    
    def post(self, *args, **kwargs):
        avatars = ["amy", "rian", "jack", "lana", "lily", "matt"] 
        slug = kwargs['slug']
        avatar_code = self.request.POST.get('selected-card')
        if avatar_code == "":
            avatar_code = "amy"
        else:
            print(avatar_code)
            avatar_code = avatars[int(avatar_code)-1]
            print(avatar_code)
        
        project_properties = ProjectProperties.objects.get(project__slug=slug)
        avatar_properties = Avatars.objects.get(name=avatar_code)

        project_properties.avatar_data = avatar_properties
        project_properties.save()

        print(self.request)
        context = {
        }
        return redirect('core:driver', slug)
    

class SelectDriver(View):
    drivers = []
    def get(self, *args, **kwargs):
        slug = kwargs['slug']
        avatar_id = ProjectProperties.objects.get(project__slug=slug)
        avatar_id = avatar_id.avatar_data.name.lower()
        print(avatar_id)

        # Retrieve data from the API
        api_key = 'cm9uYWtwcmFzYWRscDlAZ21haWwuY29t:FgOT9jdUzLhOnlQJ4zXi0'
        url = f"https://api.d-id.com/clips/actors/{avatar_id}/drivers"
        headers = {"accept": "application/json"}
        auth_headers = {
            'Authorization': f'Basic {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=auth_headers)

        if response.status_code == 200:
            data = response.json()
            drivers = data.get('clips_drivers', [])

        context = {
            'slug': slug,
             'drivers': drivers,
        }
        return render(self.request, 'drive-in.html', context)
    
    def post(self, *args, **kwargs):
        slug = kwargs['slug']
        # print(self.drivers)
        print(self.request)
        presenter_id = self.request.POST.get('selected-presenter')
        driver_id = self.request.POST.get('selected-driver')
        fetch_project_properties = ProjectProperties.objects.get(project__slug=slug)
        fetch_project_properties.presenter_id = presenter_id
        fetch_project_properties.driver_id = driver_id

        fetch_project_properties.save()
        return redirect('core:add-text', slug)

class AddText(View):
    def get(self, *args, **kwargs):
        slug = kwargs['slug']
        voices = Voices.objects.all()
        return render(self.request, 'add-text.html',{'voices': voices})
    def post(self, *args, **kwargs):
        slug = kwargs['slug']
        fetch_project_properties = ProjectProperties.objects.get(project__slug=slug)
        fetch_project_properties.text = self.request.POST.get('text-area')
        fetch_project_properties.audio_id = self.request.POST.get('voice')
        fetch_project_properties.save()

        return redirect('core:final-video', slug)



class FinalVideo(View):
    def get(self, *args, **kwargs):
        # Get the project slug from the URL parameters
        slug = kwargs.get('slug')

        # Retrieve the project by slug and check if it exists
        try:
            project = Project.objects.get(slug=slug)
            # print("Project", project.user.username)
        except Project.DoesNotExist:
            return HttpResponseNotFound("Project not found")

        # Define the path to the video file in the media directory
        user_directory = os.path.join(settings.MEDIA_ROOT, 'projects', project.user.username)
        project_directory = os.path.join(user_directory, project.slug)
        video_filename = f'{project.slug}.mp4'
        video_path = os.path.join(project_directory, video_filename)

        # Check if the video file exists
        if os.path.exists(video_path):
            # Construct the video URL based on the user ID and slug
            video_url = os.path.join('media', 'projects', project.user.username, project.slug, video_filename)

            # Render the template and pass the video URL to the frontend
            context = {
                'project': project,
                'video_url': video_url,
            }
            return render(self.request, 'final-video.html', context)
        else:
            print("Not there")
            video_url = self.get_video_url(project)
            print("v", video_url)
            context = {
                'project': project,
                'video_url': video_url,
            }
            return render(self.request, 'final-video.html', context)

    def get_video_url(self, project):
        # Define the path to save the video

        project_properties = ProjectProperties.objects.get(project=project)

        user_directory = os.path.join(settings.MEDIA_ROOT, 'projects', project.user.username)
        project_directory = os.path.join(user_directory, project.slug)
        video_filename = f'{project.slug}.mp4'
        video_path = os.path.join(project_directory, video_filename)

        # Check if the video file already exists
        # if os.path.exists(video_path):
        #     return os.path.join('media', 'projects', project.user.username, project.slug, video_filename)

        # If the video file doesn't exist, use the API to generate and download it
        api_key = 'cm9uYWtwcmFzYWRscDlAZ21haWwuY29t:FgOT9jdUzLhOnlQJ4zXi0'
        # Replace with your API key
        generate_video_url = "https://api.d-id.com/clips"

        payload = {
        "script": {
                "type": "text",
                "input": f"{project_properties.text}",
                "provider": {
                    "type": "microsoft",
                    "voice_id": f"{project_properties.audio_id}",
                    "voice_config": {
                        "style": "Cheerful"
                    }
                },
            },
            "presenter_id": f"{project_properties.presenter_id}",
            "driver_id": f"{project_properties.driver_id}",
            "background": {
                "color": "#000000"
            }
        }

        headers = {
            'Authorization': f'Basic {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(generate_video_url, json=payload, headers=headers)

        print("First call:", response.text, response.status_code)

        if response.status_code == 201:
            # Parse the response to get the clip ID
            generate_response_data = json.loads(response.text)
            clip_id = generate_response_data.get('id')
            print(clip_id)
            # Poll the API until the video status is "done"
            while True:
                get_video_url = f"https://api.d-id.com/clips/{clip_id}"
                get_response = requests.get(get_video_url, headers=headers)
                print(get_response.status_code)
                if get_response.status_code == 200:
                    get_response_data = json.loads(get_response.text)
                    if get_response_data.get('status') == "done":
                        video_url = get_response_data.get('result_url')
                        break
                #     elif get_response_data.get('status') == "error":
                #         return HttpResponseNotFound("Failed to generate video")
                # else:
                #     return HttpResponseNotFound("Failed to get video details")

                time.sleep(5)  # Wait for 5 seconds before checking again

            # Download and save the video
            video_response = requests.get(video_url)
            print(video_url)
            print("DATA:", video_response.status_code)
            if video_response.status_code == 200:
                # with open(video_path, 'wb') as video_file:
                #     video_file.write(video_response.content)
                try:
                    os.makedirs(f'{media_location}/projects/{self.request.user.username}/{project.slug}/')
                except FileExistsError:
                    # directory already exists
                    pass
                url_link = video_url
                directory_path = f'{media_location}/projects/{self.request.user.username}/{project.slug}/'
                video_name = f'{project.slug}.mp4'
                
                full_path = os.path.join(directory_path, video_name)

                urllib.request.urlretrieve(url_link, full_path)
                return os.path.join('media', 'projects', project.user.username, project.slug, video_filename)
            else:
                return HttpResponseNotFound("Failed to download video")
        else:
            return HttpResponseNotFound("Failed to generate video")
