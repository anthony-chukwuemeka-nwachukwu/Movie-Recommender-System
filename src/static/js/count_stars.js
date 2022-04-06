function getAllIds(min_required_no_of_movies_by_user, no_imdb_genres){
    document.getElementById('stared_valid').value = enoughId(min_required_no_of_movies_by_user, no_imdb_genres);
    document.getElementById('test').innerHTML = enoughId(min_required_no_of_movies_by_user, no_imdb_genres);
}


function enoughId(min_required_no_of_movies_by_user, no_imdb_genres){
    var ids = document.querySelectorAll('[id]');
    var ids_color = {};
    var stared_ids = [];
    var stars, i, arr;
    stars = document.getElementsByClassName("fa-star");

    for (i = 0; i < stars.length; i++) {

        if (String(stars.item(i).dataset.stared) == 'true'){
            stared_ids.push(stars.item(i).id);
            if (ids_color.hasOwnProperty(stars.item(i).dataset.genre)){
                ids_color[stars.item(i).dataset.genre].push(stars.item(i).dataset.stared);
            }else{
                ids_color[stars.item(i).dataset.genre] = [];
            }
        }

    }
    const ids_entries = Object.entries(ids_color);
    document.getElementById('stared_ids').value = Object.entries(stared_ids);
    var c = 0;
    for (const [k, v] of ids_entries){
        if (v.length < min_required_no_of_movies_by_user){
            return 'false';
        }
        c += 1;
    }
    return String(ids_entries.length == no_imdb_genres);
}
