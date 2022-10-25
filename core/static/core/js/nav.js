const navSlide=()=>{
    const burger = document.querySelector('nav .icon');
    const nav = document.querySelector('nav ul');

    burger.addEventListener("click", (e)=>{
        nav.classList.toggle('show');
        console.log('clicked')
    })
}

const joinInput=()=>{
    const origin = document.querySelector('#origin');
    const destination = document.querySelector('#destination');
    const date1 = document.querySelector('#time1');
    const date2 = document.querySelector('#time2');


    const final = document.querySelector('#final');
    const button = document.querySelector('#submit-button');

    button.addEventListener("click", ()=>{
         final.value = string.concat(origin.value, destination.value , " start off ", date1.value, " return on ", date2.value)
    })


}


const app=()=>{
   navSlide();
   joinInput();
}
app();




