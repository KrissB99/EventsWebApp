function showAlert(resp, data) {
    if (resp.ok) {
        const Toast = Swal.mixin({
            toast: true,
            position: "top-end",
            showConfirmButton: false,
            timer: 2000,
        });
        Toast.fire({
            icon: "success",
            title: data.detail
        });
    }
    else {
        Swal.fire({
            position: 'top-end',
            icon: 'error',
            title: data.detail ? data.detail : 'Something went wrong! Please try again.',
            showConfirmButton: false,
            timer: 1500
        })
    }
}