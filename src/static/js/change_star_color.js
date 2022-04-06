function changeStarColor(movie_id) {
  let star_id = document.getElementById(movie_id);
  
  if( star_id.style.color == 'orange' ){
      star_id.style.color = 'white';
  }
  else if(star_id.style.color == 'white'){
      star_id.style.color = 'orange';
  }
}
