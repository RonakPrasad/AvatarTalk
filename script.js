document.addEventListener("DOMContentLoaded", function () {
  const body = document.querySelector("body");
  const modal = document.querySelector(".modal");
  const modalButton = document.querySelector(".modal-button, .header-right");
  const closeButton = document.querySelector(".close-button");
  const scrollDown = document.querySelector(".scroll-down");
  let isOpened = false;

  const openModal = () => {
    modal.classList.add("is-open");
    body.style.overflow = "hidden";
  };

  const closeModal = () => {
    modal.classList.remove("is-open");
    body.style.overflow = "initial";
    // Scroll to the top of the page
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  window.addEventListener("scroll", () => {
    if (window.scrollY > window.innerHeight / 3 && !isOpened) {
      isOpened = true;
      scrollDown.style.display = "none";
      openModal();
    } else if (window.scrollY <= window.innerHeight / 3 && isOpened) {
      isOpened = false;
      scrollDown.style.display = "block";
      closeModal();
    }
  });

  modalButton.addEventListener("click", openModal);
  closeButton.addEventListener("click", closeModal);

  document.addEventListener("keydown", (evt) => {
    evt = evt || window.event;
    if (evt.keyCode === 27) {
      closeModal();
    }
  });
});

function toggleModal(state) {
  const loginContent = document.getElementById('login-content');
  const loginImage = document.getElementById('login-image');
  const signupContent = document.getElementById('signup-content');

  if (state === 'signup') {
      loginContent.style.display = 'none';
      loginImage.style.display = 'none';
      signupContent.style.display = 'block';
  } else {
      loginContent.style.display = 'block';
      loginImage.style.display = 'block';
      signupContent.style.display = 'none';
  }
}

function registerUser() {
  // Perform user registration logic here

  // After registration, toggle back to login state
  toggleModal('login');
}
