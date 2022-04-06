function changeStarColor(movie_id) {
    let star_id = document.getElementById(movie_id);
    
    if( star_id.style.color == 'orange' ){
        star_id.style.color = 'white';
    }
    else if(star_id.style.color == 'white'){
        star_id.style.color = 'orange';
    }
    //star_id.dataset.stared = col=='white'
}


function deleteLike(movie_id){
    alert(movie_id);
    var result = $.ajax({
        url: "delete_like.py",
        data: {movie_id:movie_id}
    });
    alert(result);
    return true;
}

function insertLike(movie_id,username){
    //alert("inserted");
    /*var result = $.ajax({
        url: "src/utils/production/insert_like.py",
        data: {movie_id:movie_id, username:username}
    });*/
    alert(movie_id);
    return true;
}