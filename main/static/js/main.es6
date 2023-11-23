class Main{
    constructor(){
    }

    revealUI(){
        let me=this;
        console.log("Reveal UI");
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
        $('.universe').addClass('hidden');
        $('.universe').removeClass('shown');
    }

    revealUniverse(){
        let me=this;
        console.log("Reveal Universe");
        $('.world').removeClass('shownflex');
        $('.universe').removeClass('hidden');

        $('.world').addClass('hidden');
        $('.universe').addClass('shown');
    }

    perform(){
//         $('.world').addClass('hidden');
//         $('.universe').addClass('hidden');

    }
}