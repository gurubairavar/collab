// ALERT BOX CLOSING
const CloseButtons = document.querySelectorAll(".error__close");
CloseButtons.forEach((CloseButton) =>
{
    CloseButton.addEventListener("click", ()=> {
        CloseButton.parentElement.style.display = "none";
    })
});
// CHANGING SUCCESS BAR TO ALERT
if(document.querySelector(".error__title").innerHTML == "Username or Password is incorrect")
{
    document.querySelector(".error").className = "error";
    document.querySelector(".error__icon i").classList.add("fa-exclamation-triangle");
}
// CONFIRM FORM RESUBMISSION
if ( window.history.replaceState ) 
{
  window.history.replaceState( null, null, window.location.href );
}