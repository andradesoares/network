document.addEventListener('DOMContentLoaded', function() {
  document.addEventListener('click', event => {
    if (event.target.id === 'submitPost') {
      send_post()
    }
  });
  document.addEventListener('click', event => {
    if (event.target.className === 'likeButton') {
      send_like(event.target.id)
    }
  });
  document.addEventListener('click', event => {
    if (event.target.className === 'followButton') {
      follow()
    }
  });
  document.addEventListener('click', event => {
    if (event.target.className === 'editButton') {
      editanchor(event.target.id)
    }
  });
  document.addEventListener('click', event => {
    if (event.target.className === 'cancelButton') {
      cancelpost(event.target.id)
    }
  });
  document.addEventListener('click', event => {
    if (event.target.className === 'saveButton') {
      savepost(event.target.id)
    }
  });
});

function send_post() {
  console.log("oi")
  fetch('/post', {
    method: 'POST',
    body: JSON.stringify({
        body: document.querySelector('#post-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    document.querySelector('#post-body').value = ''; 
    let postsContainer = document.querySelector(`.postsContainer`)
    postsContainer.insertBefore(
    `
      <div class="postContainer">
        <a href="{% url 'profile' ${result.post.user_id} %}"><h5> ${result.post.user_id} </h5></a>
        <div class="postBody postBody${result.post.post.id}">
          <p>${result.post.body}</p>
        </div>
          <p class="postTimestamp">${result.post.timestamp }</p>
        <div class="d-flex">
          <form class="likeButton" id="${result.post.post.id}">
            <img id="likeImage${result.post.post.id}" src="../../static/network/likeButtonWhite.png" alt="Italian Trulli">
          </form>
          <p id="postCount${result.post.post.id}">0</p>
        </div>
        <div class="d-flex" id="anchor${result.post.post.id}">
          <a class="editButton" id="${result.post.post.id}">Edit</a>
        </div>
      </div>
    `, postsContainer.childNodes[0])
    console.log(result);
  });
}

function send_like(id) {
  let postId = id
  fetch('/likes', {
    method: 'POST',
    body: JSON.stringify({
      body: postId,
    })
  })
  .then(response => response.json())
  .then(result => {
    document.querySelector(`#postCount${id}`).innerHTML = result.postCount
    if (result.like == true) {
      document.querySelector(`#likeImage${id}`).src = "../../static/network/likeButtonRed.png"
    } else {
      document.querySelector(`#likeImage${id}`).src = "../../static/network/likeButtonWhite.png"
    }
  });
}

function follow() {
  let perfil = document.querySelector("#followPerfil").value
  fetch('/follow', {
    method: 'POST',
    body: JSON.stringify({
      body: perfil,
    })
  })
  .then(response => response.json())
  .then(result => {
    if (result.follow == true) {
      document.querySelector("#followButtonId").textContent = "Unfollow"
    } else {
      document.querySelector("#followButtonId").textContent = "Follow"
    }
    document.querySelector(".folowersCount").innerHTML = `Followers: ${result.followers}`
  });
}

function editanchor(id) {
  let textArea = document.createElement('textArea');
  textArea.style.resize= 'none'
  textArea.style.width = '100%'
  let postBody = document.querySelector(`.postBody${id}`).children[0]
  textArea.innerHTML = postBody.innerHTML
  postBody.parentNode.replaceChild(textArea, postBody);
  let anchorDiv = document.querySelector(`#anchor${id}`)
  anchorDiv.innerHTML =
      `
      <div class="singleMail">
        <a class="saveButton" id="${id}">Save</a>
        <a class="cancelButton" id="${id}">Cancel</a>
      </div>
      `

}

function cancelpost(id) {
  let postBody = document.createElement('p');
  let textArea = document.querySelector(`.postBody${id}`).children[0]
  postBody.innerHTML = textArea.innerHTML
  textArea.parentNode.replaceChild(postBody, textArea);
  let anchorDiv = document.querySelector(`#anchor${id}`)
  anchorDiv.innerHTML =
      `
      <div class="singleMail">
        <a class="editButton" id="${id}">Edit</a>
      </div>
      `
}

function savepost(id) {
  let postId = id
  let textArea = document.querySelector(`.postBody${id}`).children[0].value
  fetch('/save', {
    method: 'POST',
    body: JSON.stringify({
      body: textArea,
      id:postId
    })
  })
  .then(response => response.json())
  .then(result => {
    let postBody = document.createElement('p');
    let textAreabody = document.querySelector(`.postBody${id}`).children[0]
    postBody.innerHTML = textArea
    textAreabody.parentNode.replaceChild(postBody, textAreabody);
    let anchorDiv = document.querySelector(`#anchor${id}`)
    anchorDiv.innerHTML =
        `
        <div class="singleMail">
          <a class="editButton" id="${id}">Edit</a>
        </div>
        `
  });
}