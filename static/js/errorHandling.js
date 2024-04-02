axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    let errorMessage = "An unexpected error occurred."; // Default error message

    if (error.response && error.response.data && error.response.data.error) {
      errorMessage = error.response.data.error;
    } else if (error.message) {
      errorMessage = error.message;
    }

    // Display the error message
    $("#errorModal .modal-body").text(errorMessage);
    $("#errorModal").modal("show");

    return Promise.reject(error);
  }
);

function showError(error) {
  if (error.response && error.response.data && error.response.data.error) {
    errorMessage = error.response.data.error;
  } else if (error.message) {
    errorMessage = error.message;
  } else {
    errorMessage = error;
  }

  $("#errorModal .modal-body").text(errorMessage);

  // Show the modal
  $("#errorModal").modal("show");
}
