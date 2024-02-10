class Piani extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.gdr = false
        this.name = "piani";
        this.parent = "#svg_area";
        if ("gdr" in config){
            this.gdr = true;
        }
    }

    init() {
        super.init();
        let me = this;

        me.co.revealUI();
        me.selection = [];
        me.step = 50;
        me.fontSize = 0.3*me.step + "pt";
        // Drawing Size
        me.height = me.step * 21.0
        me.width = me.step * 29.7
        me.ox = 0.85
        me.oy = 0.5
        // View Size
        let boundingBox = document.querySelector("#svg_area").getBoundingClientRect();
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));

        me.fontsize = me.step / 4 ;
        me.cardset = []


        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("class", "vis")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h);
        me.svg = me.vis.append('g')
            .attr("class", "svg")
            .attr("id", me.code)
            .attr("width", me.width)
            .attr("height", me.height)
            .append("svg:g")
            .attr("transform", "translate(0,0)")
        ;
        console.log(me.name+" initialized..." );
    }


    drawBack(){
        let me = this;
        me.back = me.svg.append('g')
            .attr("class","mapback")
            .append("g")
        ;
    }


    zoomActivate() {
        console.log("Desactivate standard modulo zoom just in case...")
    }

   register(){
        super.register();
        let me = this;
        me.co.axiomaticPerformers.push(me);
    }

    drawAll(){
        let me = this;
        me.drawBack();
        me.drawPicture()
    }

    drawPicture(){
        let me = this;
        let link_name = me.filename.replace("dragonade_media","media")
        $('.panzoom').remove();

        $(me.parent).prepend(`<image class='panzoom' src=${link_name}/>`);

        PanZoom(".panzoom",{minScale: 0.01, maxScale: 8, increment: 0.1, liner: false})
//         me.picture = me.back.append('svg:image')
//             .attr("x",0)
//             .attr("y",0)
//             .attr("width",wi)
//             .attr("height",hi)
//             .attr('xlink:href', link_name)
//             .style('stroke', "#101010")
//             .style('stroke-width', "2pt")
//             ;


    }






    perform(code){
        super.perform();
        let me = this;
        me.init();
        me.filename = atob(code)
        console.log(me.filename)
        me.drawAll();

    }
}