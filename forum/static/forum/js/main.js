let baseUrl = 'https://neurobiologia.pythonanywhere.com/';

function fetchComments(postId, commentDiv, userId) {
    fetch(`${baseUrl}forum/posts/${postId}/comments/`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById("csrfToken").value 
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(comment => {
            const commentElement = document.createElement('div');
            
            if (comment.user == userId) {
                commentElement.className = 'users-comment'
                commentElement.innerHTML = `<strong>${comment.author_username}</strong>: ${comment.text}`;
            } else {
                commentElement.className = 'others-comment-wrapper';
                
                const avatarImg = document.createElement('img');
                avatarImg.src = comment.profile_image;
                avatarImg.className = 'others-avatar';
                commentElement.appendChild(avatarImg);
                
                const textDiv = document.createElement('div');
                textDiv.className = 'others-comment';
                textDiv.innerHTML = `<strong>${comment.author_username}</strong>: ${comment.text}`;
                commentElement.appendChild(textDiv);
            }
            
            commentDiv.appendChild(commentElement);
        });
    });
}

function addComment(postId, inputComment, commentDiv, userId) {
    fetch(`${baseUrl}forum/posts/${postId}/comments/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById("csrfToken").value 
        },
        body: JSON.stringify({
            "text": inputComment.value,
            "user": userId,
            "post" : postId
        })
    })
    .then(response => {
        if (!response.ok) {
            response.text().then(text => {
                console.log('Server response:', text);
            });
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        const newCommentElement = document.createElement('div');
        if (data.user == userId) {
            newCommentElement.className = 'users-comment';
        } else {
            newCommentElement.className = 'others-comment-wrapper';
        }
        newCommentElement.innerHTML = `<strong>${data.author_username}</strong>: ${data.text}`;
        commentDiv.appendChild(newCommentElement);
        inputComment.value = '';
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

function handlePostComments() {
    document.querySelectorAll('.post').forEach(element => {
        element.addEventListener('click', (event) => {
            if (event.target.tagName.toLowerCase() === 'textarea' || event.target.tagName.toLowerCase() === 'a') {
                return;
            }
            let existingCommentDiv = event.currentTarget.nextElementSibling;

            if (existingCommentDiv && existingCommentDiv.classList.contains('comment-div')) {
                // Sprawdzenie, czy comment-div jest otwarty
                if (existingCommentDiv.classList.contains('show-animation') || !existingCommentDiv.classList.contains('hide-animation')) {
                    existingCommentDiv.classList.remove('show-animation');
                    existingCommentDiv.classList.add('hide-animation');
                    existingCommentDiv.addEventListener('animationend', () => {
                        if (existingCommentDiv.classList.contains('hide-animation')) {
                            existingCommentDiv.remove();
                        }
                    });
                } else {
                    existingCommentDiv.classList.add('show-animation');
                    existingCommentDiv.classList.remove('hide-animation');
                }
                return;
            }
            
            const commentDiv = document.createElement('div');
            commentDiv.classList.add('comment-div', 'show-animation');  // Dodajemy klasę animacji od razu
            const inputComment = document.createElement('textarea');
            const postId = event.currentTarget.dataset.postId;
            const userId = document.getElementById('user-data').getAttribute('data-user');

            fetchComments(postId, commentDiv, userId);

            inputComment.addEventListener('keydown', (event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    addComment(postId, inputComment, commentDiv, userId);
                }
            });

            event.currentTarget.insertAdjacentElement('afterend', commentDiv);
            commentDiv.appendChild(inputComment);
        });
    });
}


function displayProfileElements () {
    const posts = document.querySelector("#posts");
    const new_post = document.querySelector("#input_container");
    if (display_posts !== "all"){
        new_post.style.display = "none";
        posts.style.margin = "0 200px 100px 50px";
    }else{
        const post_fontainee = document.querySelector('.main-body-container');
        const followers_container = document.querySelector('#followers_container');
        post_fontainee.style.display = "block";
        followers_container.style.display = "none"
        posts.style.width = "75%";
        new_post.style.width = "75%";
        posts.style.margin = "0 auto 10px auto";
        new_post.style.margin = "0 auto 10px auto";
    }
};

function handleFollowingClick(event) {
    event.preventDefault(); 

    display_posts = 'following';

    fetch(`${baseUrl}forum/posts/?username=${display_posts}&page=${currentPage}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        setupPagination(data.count); 
        document.querySelector('#posts').innerHTML = '';
        data.results.forEach(post => {
            const postDiv = createPostDiv(post);
            document.querySelector('#posts').append(postDiv); 
        })
        disablePaginatorButtons();
    })
    .catch(error => {
        console.error('There was an error fetching the posts:', error);
    });
}

function sendNewPost() {
    const input = document.querySelector('#new-post-field');
  
    input.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendPost(input);
        }
    });

    const button = document.getElementById('send-post-btn');
    button.addEventListener('click', function() {
        sendPost(input);
    });
}

function sendPost(input) {
    const userDataElement = document.getElementById('user-data');

    fetch(`${baseUrl}forum/posts/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById("csrfToken").value 
        },
        body: JSON.stringify({
            "body": input.value,
            "author" :  userDataElement.getAttribute('data-user')
        })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Server response:', response.statusText);
            return response.text().then(text => {
                throw new Error(text);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        loadPosts(currentPage);
        input.value = ''; 
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function likePost(postId) {
    fetch(`${baseUrl}forum/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById("csrfToken").value 
        },
    })
    .then(response => {
        if (!response.ok) {
            console.error('Server response:', response.statusText);
            return response.text().then(text => {
                throw new Error(text);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        loadPosts(currentPage);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};

function changePostListener(element, input_body, post, event) {
    event.stopPropagation()
    element.style.display = "none";
    input_body.style.display = "block";
    input_body.autoFocus = true;
    input_body.addEventListener('keydown', function(event){
        if (event.key === "Enter"){
            const body = input_body.value;
            fetch(`${baseUrl}forum/posts/${post.id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById("csrfToken").value 
                },
                body: JSON.stringify({
                    "id": post.id,
                    "author" : post.author,
                    "author_username" : post.author_username,
                    "body": body,
                    "created_at" : post.created_at,
                    "profile_image" : post.profile_image
                })
            })
            .then(response => response.json())
            .then(data => {
                element.style.display = "block";
                input_body.style.display = "none";
                loadPosts(currentPage);
            });
            
        }
        });
    };

function setupPagination(totalPosts) {
    let postsPerPage = 10;
    totalPages = Math.ceil(totalPosts / postsPerPage);
    const pagination = document.querySelector('.pagination');
    

    pagination.innerHTML = `
        <li id="prev-button"><a class="page-link">Previous</a></li>
        <li id="next-button"><a class="page-link">Next</a></li>
    `;

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('a');
        const list_item = document.createElement('li');
        button.className = "page-link";
        button.innerHTML = i;
        button.addEventListener('click', () => {
            currentPage = i;
            loadPosts(i);
        });
        list_item.className = "page-item";
        list_item.append(button);
        let childrens = pagination.children;
        let before_last = childrens[childrens.length - 1];
        pagination.insertBefore(list_item, before_last);
    }
    document.querySelector('#prev-button').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage -= 1;
            loadPosts(currentPage);
        }
    });
    
    document.querySelector('#next-button').addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage += 1;
            loadPosts(currentPage);
        }
    });
}

function disablePaginatorButtons() {
    if (currentPage === 1) {
        document.querySelector('#prev-button').className = "page-item disabled";
    } else {
        document.querySelector('#prev-button').className = "page-item";
    }
    
    if (currentPage === totalPages) {
        document.querySelector('#next-button').className = "page-item disabled";
    } else {
        document.querySelector('#next-button').className = "page-item";
    }
}


function loadPosts(pageNumber) {
    fetch(`${baseUrl}forum/posts/?username=${display_posts}&page=${pageNumber}`)
    .then(response => response.json())
    .then(data => {
        setupPagination(data.count); 
        document.querySelector('#posts').innerHTML = '';
        data.results.forEach(post => {
            const postDiv = createPostDiv(post);
            document.querySelector('#posts').append(postDiv); 
        });
        handlePostComments();
        disablePaginatorButtons();
    });
}

function createPostDiv(post) {
    const postDiv = document.createElement('div');
    postDiv.className = "post";

    const comment_container = document.createElement('div');
    const author_container = document.createElement('div');
    const author = document.createElement('a');
    const body = document.createElement('p');
    const input_body = document.createElement('textarea')
    const created_at = document.createElement('p');
    const image = document.createElement('img');
    const likes_container = document.createElement('div')
    const likes_image = document.createElement('img')
    const likes = document.createElement('p')
    
    author.href = `${baseUrl}forum/profile/${post.author_username}/`; 
    author.innerHTML = `<strong>${post.author_username}</strong>`;
    author.style.textAlign = 'center';
    author.addEventListener('click', function(event) {
        event.stopPropagation();
    });
    body.innerHTML = `${post.body}`;
    input_body.innerHTML = `${post.body}`;
    input_body.className = 'textara_field';
    input_body.autoFocus = true;
    input_body.style.display = 'none';

    created_at.innerHTML = `Posted: ${post.created_at}`;
    created_at.style.fontSize = '10px';
    image.src = post.profile_image;

    likes_image.src = heartImageUrl;
    likes_image.id = "heart-image";
    likes.innerHTML = post.likes;
    likes.className = 'likes-number';
    likes_container.className = "likes-container"
    likes_container.addEventListener('click', (event) => {
        event.stopPropagation();  
        likePost(post.id);
    });
    likes_container.append(likes_image, likes);
    const username = document.getElementById('user-data').getAttribute('data-username');
    if (post.author_username === username) {
        const edit_button = document.createElement('button');
        edit_button.innerText = "Edit";  
        edit_button.className = "edit_btn"
        edit_button.onclick = (event) => changePostListener(comment_container, input_body, post, event); 
        comment_container.append(edit_button);
    }
    author_container.className = "author_container";
    author_container.append(image, author, created_at, likes_container);
    
    comment_container.className = "comment_container";
    comment_container.append(body);

    postDiv.append(author_container, comment_container, input_body);
    postDiv.dataset.postId = post.id;
    
    return postDiv;
}

let currentPage = 1; 
let totalPages;

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('following_url').addEventListener('click', handleFollowingClick);
    sendNewPost();
    displayProfileElements();
    loadPosts(currentPage);
});