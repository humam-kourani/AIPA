const disableEditing = true;
const enable_sending_submodel = false;

window.onload = function () {
  if (disableEditing) {
    document.body.classList.add("disable-edit");
  } else {
    document.body.classList.remove("disable-edit");
  }
};
