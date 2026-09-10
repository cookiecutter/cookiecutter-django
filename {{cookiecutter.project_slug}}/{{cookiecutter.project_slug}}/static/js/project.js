/* Project specific Javascript goes here. */

// Dismiss Django messages (templates/partials/messages.html) without reloading the page.
document.addEventListener('click', (event) => {
  const dismiss = event.target.closest('[data-dismiss]');
  if (dismiss) {
    dismiss.closest('[role="alert"]').remove();
  }
});
