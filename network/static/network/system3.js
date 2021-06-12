
function like(post_id){
    fetch(`/like/${post_id}`,{
        method: "PUT",
        body: JSON.stringify({
            "message": "Just Liked from Javascript."
        }) 
    })
    .then(function (response){
        if (response.ok){
            console.log(response)
            console.log("Reaching Get Request.")
            fetch(`/like/${post_id}`)
            .then(response => response.json())
            .then(item => {
                if (item.like || item.like >= 0){
                    console.log("TESTING 2")
                    $('.'+ post_id +'-text').text(`${item.like}`)
                
                    if ( item.check_like == true){
                        $('.' + post_id + '-btn').text('Unlike')
                    } else {
                        $('.' + post_id + '-btn').text('Like')
                    } 
                }

            })
            return response.json()
        } else{
            console.log(response)
            return Promise.reject(response)
        }
    }).catch(function(err){
        console.log(err)
        console.warn('There is an error.')
    })

    console.log("Request sent successfully.")
    
}


function follow (){
    var user_profile = $('.user-profile').text()

    fetch(`/follow/${user_profile}`)
    .then(response => response.json())
    .then(data => {
        if (data.following_check == true){
            $('.follow').text('Unfollow')
        } else {
            $('.follow').text('Follow')
        }
    })
    .catch(err => {
        console.log(err)
    })

    
}
