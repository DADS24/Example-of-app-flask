$(document).ready(() =>{
    let a = $(".listElement");//has the real element not a clone, if we use clone won't delete anything cuz we are working with a copy
    console.log(a);
    
    $(".but1").click((e)=>{
        $(e.target).closest(a).remove()//removes the closest element with specific class to the child element      
         
    })
    axios.get('http://localhost:5000/lista')
        .then((listaDeCosas)=>{
            
            listaDeCosas['data'].forEach((e)=>{
                let a = $(".listElement:first").clone()
                a[0].querySelector('.name').innerHTML= e['nombre']
                a[0].querySelector('.ape').innerHTML= e['precio']
                console.log(e);
                
                a.appendTo('.mainDiv')

            })
            
        })
        .catch((err)=>{
            console.log(err);
            
        })
})

