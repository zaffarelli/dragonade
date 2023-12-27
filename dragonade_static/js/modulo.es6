class Modulo {
    constructor(co, config) {
        this.co = co;
        this.config = config;
        this.name = "Modulo";
    }

    init() {
        let me = this;
        console.log(me.name+" Init");
        me.debug = true;
    }

    softLog(txt){
        let me = this;
        me.co.softLog(me.name,txt);
    }

    hardLog(txt){
        let me = this;
        me.co.hardLog(me.name,txt);
    }

    register(){
        let me = this;
        me.co.modules.push(me);
        console.log(me.name+" Registered");
    }

    perform() {
        let me = this;
        console.log(me.name+" Perform");
    }
}