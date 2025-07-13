document.addEventListener('click', function(event) {
    if (event.target.classList.contains('backwards')) {
        localStorage.setItem('viewTransitionType', 'backwards');
    }
    else {
        localStorage.setItem('viewTransitionType', 'forwards');
    }
});

window.addEventListener("pagereveal", async (e) => {
    if (e.viewTransition) {
      e.viewTransition.types.add(localStorage.viewTransitionType);
    }
  });