// small UX: disable button on submit to prevent double submits
document.addEventListener('DOMContentLoaded', function(){
  const form = document.querySelector('.contact-form');
  if(form){
    form.addEventListener('submit', function(){
      const btn = form.querySelector('button[type="submit"]');
      if(btn) {
        btn.disabled = true;
        btn.innerText = 'Sending...';
      }
    });
  }
});
