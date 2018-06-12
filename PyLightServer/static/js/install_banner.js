let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  // Update UI notify the user they can add to home screen
  //btnAdd.style.display = 'block';
});

window.addEventListener('appinstalled', (evt) => {
  app.logEvent('a2hs', 'installed');
});