var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var movieId = this.dataset.movie
		var action = this.dataset.action
		console.log('movieId:', movieId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			console.log('not loged in')
		}else{
			updateUserOrder(movieId, action)
		}
    })
}  

function updateUserOrder(movieId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'movieId':movieId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
			console.log('data:', data)
			location.reload()
		});
}

