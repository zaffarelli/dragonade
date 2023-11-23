class Main{
    constructor(){
    }

    revealUI(){
        let me=this;
        $('world').addClass('shownflex');
        $('universe').addClass('hidden');
    }

    revealUniverse(){
        let me=this;
        $('world').addClass('hidden');
        $('universe').addClass('shown');
    }

    perform(){

    }
}