console.log('is this working?')

const copyBtns = [...document.getElementsByClassName('copy-btn')]
console.log(copyBtns)


let previous = null 

copyBtns.forEach(btn=> btn.addEventListener('click',()=>{
    console.log('click')
    const address = btn.getAttribute('data-hex')
    console.log(address)
    navigator.clipboard.writeText(address)
    btn.textContent = 'copied'

    navigator.clipboard.readText().then(clipText =>{


        console.log(clipText)
        btn.textContent = 'address copied'
    })

    if (previous) {
        previous.textContent = 'click'

    }

    previous = btn
}))


function showLoaderOnClick(url) {
    showLoader();
    window.location=url;
}
function showLoader(){
    $('body').append('<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>');
}





