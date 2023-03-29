 async function loadComments(){
    const comments = document.getElementById('comments')
    const url = '/foro/subreddit/post/comment-json/'
    const options = {
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin'
    }
  
    // add request body
    var formData = new FormData();
    formData.append('slug', comments.dataset.postSlug);
    options['body'] = formData;
  
    // wait for Moment.js to load
    // se crea uan promesa explicita ya que moment() no es compatible con async y await
    // si fuera compatible solo seria necesario hacer esto `await moment()`
      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
  
    // send HTTP request
    fetch(url, options)
    .then(response => response.json())
    .then(data => {
      data.data.forEach(item=>{
        const li = document.createElement("li");
        const timeSince = moment(item.created).fromNow();
  
        if (item.is_parent) {
          // console.log('ENTRO');
          let html = 
          `
          <div class="flex space-x-3 py-3 border-t border-red-600">
            <div class="flex-shrink-0">
              <img class="h-10 w-10 rounded-full" src="${ item.thumbnail }" alt="">
            </div>
            <div>
              <div class="text-sm">
                <a href="#" class="font-medium text-gray-900 user-name" data-username="${ item.name }">${ item.name }</a>
              </div>
              <div class="mt-1 text-sm text-gray-700">
                <p>${ item.body }</p>
              </div>
              <div class="mt-2 text-sm space-x-2">
                <span class="text-gray-500 font-medium">${ timeSince } ago</span>
                <span class="text-gray-500 font-medium">&middot;</span>
                <button type="button" class="text-gray-900 font-medium button-reply">Reply</button>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 py-6 hidden display-reply">
          <div class="min-w-0 flex-1">
            <form id="formReplyComment" data-id="${item.id}" action=".">
              <div>
              <label for="comment" class="sr-only">About</label>
              <textarea id="comment" name="comment" rows="3" class="shadow-sm block w-full focus:ring-blue-500 focus:border-blue-500 sm:text-sm border border-gray-300 rounded-md comment-reply" placeholder="Add a note"></textarea>
              </div>
              <div class="mt-3 flex items-center justify-between">
                <a href="#" class="group inline-flex items-start text-sm space-x-2 text-gray-500 hover:text-gray-900">
                  <!-- Heroicon name: solid/question-mark-circle -->
                  <svg class="flex-shrink-0 h-5 w-5 text-gray-400 group-hover:text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                  </svg>
                  <span> Some HTML is okay. </span>
                </a>
                <button type="submit" class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Comment</button>
              </div>
            </form>
          </div>
        </div>
        
          `

          for(let children of item.children){
            const timeSince = moment(children.created).fromNow();
            html+= 
            `
              <div class="flex space-x-3 py-3 ml-6 lg:ml-12">
                <div class="flex-shrink-0">
                  <img class="h-10 w-10 rounded-full" src="${ children.thumbnail }" alt="">
                </div>
                <div>
                  <div class="text-sm">
                    <a href="#" class="font-medium text-gray-900">${ children.name }</a>
                  </div>
                  <div class="mt-1 text-sm text-gray-700">
                    <p>${ children.body }</p>
                  </div>
                  <div class="mt-2 text-sm space-x-2">
                    <span class="text-gray-500 font-medium">${ timeSince } ago</span>
                    <span class="text-gray-500 font-medium">&middot;</span>
                    <button type="button" class="text-gray-900 font-medium button-reply">Reply</button>
                  </div>
                </div>
              </div>
            
            `
          }

          li.innerHTML=html
          const child = li
          comments.appendChild(child)
        

        }

        // const commentText = document.querySelector('.comment-text');
        // const usernameRegex = /@(\S+)/g;
        // const commentHTML = commentText.innerHTML;
        // const newCommentHTML = commentHTML.replace(usernameRegex, '<a href="/profile/$1">@$1</a>');
        // commentText.innerHTML = newCommentHTML;

          // Local
          // li.querySelector('.button-reply')
          //   .addEventListener('click', function(e){
          //     const displayReply = li.querySelector('.display-reply')
          //     displayReply.classList.toggle('hidden');
          //     const commentReply = displayReply.querySelector('.comment-reply')
          //     commentReply.value = `@${item.name} `;
          //     commentReply.focus();
          //   })
    
  
      })
      
      // Gobal
      comments.querySelectorAll('li')
              .forEach(comment=>{
                comment.querySelector('.button-reply')
                       .addEventListener('click', function(e){
                          const displayReply = comment.querySelector('.display-reply')
                          displayReply.classList.toggle('hidden');
                          const commentReply = displayReply.querySelector('.comment-reply')
                          const userName = comment.querySelector('.user-name').dataset.username;
                          commentReply.value = `@${userName} `;
                          commentReply.focus();
                       })

                const formReplyComment = comment.querySelector("#formReplyComment")
                formReplyComment.addEventListener("submit", function(e){
                                    console.log('chee');
                                    e.preventDefault()
                        
                                    const url = '/foro/subreddit/post/comment-json/'
                                    const options = {
                                      method: 'POST',
                                      headers: {'X-CSRFToken': csrftoken},
                                      mode: 'same-origin'
                                    }
                        
                                    // const editor = CKEDITOR.instances.id_body;
                                    // const text = editor.getData();
                                    // const text = editor.document.getBody().getText();
                                    // console.log(text);
                                    
                                    const displayReply = comment.querySelector('.display-reply')
                                    const commentReply = displayReply.querySelector('.comment-reply')
                                    const text = commentReply.value;

                                    // add request body
                                    const formData = new FormData()
                                    formData.append('slug', comments.dataset.postSlug);
                                    formData.append('action', 'create_comment');
                                    formData.append('parent', formReplyComment.dataset.id);
                                    formData.append('body', text);
                                    options['body'] = formData;
                        
                        
                                    // send HTTP request
                                    fetch(url, options)
                                    .then(response=>response.json())
                                    .then(data=>{
                                      if (data['status'] === 'ok'){ 
                                        document.getElementById('comments').innerHTML = ''
                                        loadComments();
                                      }
                                      console.log(data);
                                    })
                      
                      
                                })
              })
      

  
    })
  }

  loadComments();


  // Parent Comment
  document.getElementById("formComment")
          .addEventListener("submit", function(e){
            e.preventDefault()

            const url = '/foro/subreddit/post/comment-json/'
            const options = {
              method: 'POST',
              headers: {'X-CSRFToken': csrftoken},
              mode: 'same-origin'
            }

            const editor = CKEDITOR.instances.id_body;
            const text = editor.getData();
            // const text = editor.document.getBody().getText();
            console.log(text);

            // add request body
            const formData = new FormData()
            formData.append('slug', comments.dataset.postSlug);
            formData.append('action', 'create_comment');
            formData.append('body', text);
            options['body'] = formData;


            // send HTTP request
            fetch(url, options)
            .then(response=>response.json())
            .then(data=>{
              if (data['status'] === 'ok'){ 
                document.getElementById('comments').innerHTML = ''
                editor.setData('')
                CKEDITOR.timestamp='ABCD';
                loadComments();
              }
              console.log(data);
            })

          
          })



    // setTimeout(()=>{
    //   // show or hidden comment
    //   document.querySelectorAll('.show-reply')
    //   .forEach(reply=>{
    //     console.log(reply);
    //     reply.addEventListener('click', function(e){
    //       alert('x')
    //     })
    //   })
    // }, 2000)

    // window.addEventListener('load', function(){
    //   // show or hidden comment
    //   document.querySelectorAll('.show-reply')
    //   .forEach(reply=>{
    //     console.log(reply);
    //     reply.addEventListener('click', function(e){
    //       alert('x')
    //     })
    //   })
    // })

    // window.onload = function(){
 
    // }
          

    

  // Child comment

  // document.getElementById("formReplyComment")
  //         .addEventListener("submit", function(e){
  //           e.preventDefault()

  //           const url = '/foro/subreddit/post/comment-json/'
  //           const options = {
  //             method: 'POST',
  //             headers: {'X-CSRFToken': csrftoken},
  //             mode: 'same-origin'
  //           }

  //           const editor = CKEDITOR.instances.id_body;
  //           const text = editor.getData();
  //           // const text = editor.document.getBody().getText();
  //           console.log(text);

  //           // add request body
  //           const formData = new FormData()
  //           formData.append('slug', comments.dataset.postSlug);
  //           formData.append('action', 'create_comment');
  //           formData.append('parent', );
  //           formData.append('body', text);
  //           options['body'] = formData;


  //           // send HTTP request
  //           fetch(url, options)
  //           .then(response=>response.json())
  //           .then(data=>{
  //             if (data['status'] === 'ok'){ 
  //               document.getElementById('comments').innerHTML = ''
  //               editor.setData('')
  //               CKEDITOR.timestamp='ABCD';
  //               loadComments();
  //             }
  //             console.log(data);
  //           })


  //         })