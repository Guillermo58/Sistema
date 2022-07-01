function denegar(id) {
	swal.fire({
	  "title": "¿Estas seguro?",
	  "text": "Estas a punto de denegar una cuenta que luego no podras recuperar!",
	  "icon": "warning",
	  "showCancelButton": true,
	  "cancelButtonText": "No, cancelar",
	  "confirmButtonText": "Si, eliminar",
	  "confirmButtonColor": "#dc3545",
	  "reverseButtons": true,
	})
	  .then(function (result) {
		if (result.isConfirmed) {
		  window.location.href="denegar?id="+id
		  swal.fire({
			"title": "Ni modito :c",
			"text": "La solicitud ha sido denegada",
			"icon": "success"
		  })
		} else {
		  swal.fire({
			"text": "La solicitud esta resguardada",
			"icon": "success",

		  });
		}
	  });
  }