function showAddTodo(){
    const addOverlay = document.querySelector("#add-overlay");
    addOverlay.style.display = "flex";
}

function hideAddTodo(){
    const addOverlay = document.querySelector("#add-overlay");
    addOverlay.style.display = "none";
}

async function deletemeTodo(event){
    const tr = event.target;

    const todo_div = tr.closest(".todo");   
    const todo_id = todo_div.id;
    todo_div.remove();
    await fetch("/deleteTodo",{
        method:"POST",
        headers:{"Content-Type":"application/json",},
        body:JSON.stringify({
            id:todo_id
        })
    })
}

let current_editing_id = 0

function showEditTodo(event){
    // making the popup to display
    const editOverlay = document.querySelector("#edit-overlay");
    editOverlay.style.display = "flex";
    
    // fetching the todo id
    const todo_div = event.target.closest(".todo");
    current_editing_id = todo_div.id;
    
    // fetching the current task and status 
    const tr = event.target.closest(".todo");
    const current_task = tr.querySelector(".content").textContent;
    const current_status = tr.querySelector(".status").textContent;
    
    
    // opening popup with current task and status data
    editOverlay.querySelector("textarea").value = current_task;
    editOverlay.querySelector("input[name='status']").value = current_status;

}
async function updateTodo(event){

    event.preventDefault();
    const form = event.target;    
    const task = form.querySelector("textarea").value;
    const status = form.querySelector("input[name='status']").value;
    const tag = form.querySelector("select[name='tag']").value;
    
    const response = await fetch("/editTodo",{
        method:"POST",
        headers:{"Content-Type":"application/json",},
        body:JSON.stringify({
            id:current_editing_id,
            task:task,
            status:status,
            tag:tag
        })
    })

    if(response.ok){
        const result = await response.json();
        window.location.href = result.redirect;
    }
    else{
        console.log("failer to update");
    }

}

function hideEditTodo(){
    const addOverlay = document.querySelector("#edit-overlay");
    addOverlay.style.display = "none";
}
