class Combattimento extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.name = "Combattimento";
        this.parent = "#svg_area";
        console.log("Combattimento loaded!!")
    }

    init() {
        super.init();
        let me = this;
        me.version = "0.1";
        me.supertitle = "";
        me.fontSize = me.step / 6;
        // Drawing Size
        me.height = me.step * 21.0
        me.width = me.step * 29.7/2
        me.ox = 0
        me.oy = 0
        // View Size
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));
        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h);
        me.svg = me.vis.append('g')
            .attr("id", me.code)
            .attr("width", me.width)
            .attr("height", me.height)
            .append("svg:g")
            .attr("id","print_area")
            .attr("transform", "translate(0,0)")
        ;
    }

    drawPrelude(){
        let me = this
    }

    drawRounds(){
        let me = this
        me.rounds = me.back.append("g")
            .attr("class","rounds")
            .data(me.data.rounds)
            .select(".round")
        me.round = me.rounds.append("")
            .attr("class","round")
            .attr("id",(d,i) => "round_"+d.id )
    }

    drawEpilogue(){
        let me = this
    }


    drawCombat(){
        let me = this
        me.drawPrelude()
        me.drawRounds()
        me.drawEpilogue()
    }

    addEvent(){
    }



    perform(){
        super.perform()
        let me = this
        me.drawCombat();
    }

}