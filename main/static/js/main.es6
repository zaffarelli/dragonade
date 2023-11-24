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
        let me = this;
//         $('.world').addClass('hidden');
//         $('.universe').addClass('hidden');
        me.registerActions();
    }

    registerActions(){
        let me = this;
        me.registerEditables();
    }

    registerEditables(){
        let me = this;
        $('.editable').off().on('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            if (e.ctrlKey){
                let action = $(this).attr('action');
                let id = $(this).attr('id');
                console.log(action);
                console.log(id);
            }
        });
    }
}