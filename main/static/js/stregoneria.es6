class Stregoneria extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.name = "Stregoneria";
        this.parent = "#svg_area";
    }

    init() {
        super.init();
        let me = this;
        me.version = "0.8";
        me.supertitle = "";
        // Drawing Size
        me.height = me.step * 21.0
        me.width = me.step * 29.7
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

    drawStregoneria(){
        let me = this;
        let s = {}
        _.forEach(me.config.data, (v,k) => {
            if (v.rid == me.code){
                s = v
                return false
            }
        });
        let ox = 0.5, oy = 1.5
        // Statistics
        me.stregoneria = me.back.append("g")
            .attr("class","stregoneria")
            .attr("id","stregoneria_"+s.rid)
            .attr("transform","translate("+ox*me.step+","+oy*me.step+")")
//         me.stregoneria.append('rect')
//             .attr("class","full_box")
//             .attrs({"x":0.5, "y":1.5*me.step,"rx":me.step*0.5,"ry":me.step*0.5,"width":me.step*14,"height":me.step*20})
//             .style("fill", "none")
//             .style("stroke", "#202020")
//             .style("stroke-width", "3pt")

        me.stregoneria.append('rect')
            .attr("class","rect_top")
            .attrs({"x":0, "y":me.step*0,"rx":me.step*0.05,"ry":me.step*0.05,"width":me.step*14,"height":me.step*2.75})
            .style("fill", "none")
            .style("stroke", "#808080")
            .style("stroke-width", "3pt")
        me.stregoneria.append('rect')
            .attr("class","rect_bottom")
            .attr("id","rectbot")
            .attrs({"x":0, "y":me.step*3,"rx":me.step*0.05,"ry":me.step*0.05,"width":me.step*14,"height":me.step*2.75})
            .style("fill", "none")
            .style("stroke", "#808080")
            .style("stroke-width", "3pt")
        me.stregoneria.append('text')
            .attrs({"x":me.step*0.25, "y":(-0.25)*me.step})
            .styles({"font-family":"Are You Serious", "font-size":me.fontSize*4+"pt", "text-anchor":"start"})
            .text(s.name)
        me.stregoneria.append('text')
            .attrs({"x":me.step*13.75, "y":-0.25*me.step})
            .styles({"font-family":"Wellfleet", "font-size":me.fontSize*4+"pt", "text-anchor":"end"})
            .text(s.puissance)

        let lh = 0.425*2/3*me.step
        let stack_y = 7
        let text_metrics = [
            {"x":0.25, "y":0.5, "label":"Catégorie", "value":s.category+" (Voie: "+s.path+")","id":"des1"},
            {"x":0.25, "y":1.0, "label":"Jet", "value":"Rêve + "+s.roll,"id":"des2"},
            {"x":0.25, "y":stack_y, "label":"Description", "value": s.description,"id":"des4" },
            {"x":0.25, "y":stack_y, "label":"Composantes", "value": s.composantes,"id":"des5" },
            {"x":0.25, "y":stack_y, "label":"Autres noms", "value": s.alternative_names,"id":"des6" },
        ]
        let delx = 3.25
        let metrics = [
            {"x":(delx * 0) + 0.25, "y":1.5, "label":"Difficulté", "value":s.diff,"id":s.rid+"met1"},
            {"x":(delx * 1) + 0.25, "y":1.5, "label":"Points de Rêve", "value":s.dps,"id":s.rid+"met2"},
            {"x":(delx * 2) + 0.25, "y":1.5, "label":"Résistance", "value":s.resistance,"id":s.rid+"met3"},
            {"x":(delx * 3) + 0.25, "y":1.5, "label":"TI", "value":s.ti,"id":s.rid+"met4"},
            {"x":(delx * 0) + 0.25, "y":2.0, "label":"Portée", "value":s.range,"id":s.rid+"met5"},
            {"x":(delx * 1) + 0.25, "y":2.0, "label":"Durée", "value":s.duration,"id":s.rid+"met6"},
            {"x":(delx * 2) + 0.25, "y":2.0, "label":"Coût en Songe", "value":s.songe,"id":s.rid+"met7"},
            {"x":(delx * 3) + 0.25, "y":2.0, "label":"", "value":"","id":s.rid+"met8"},
        ]
        _.forEach(text_metrics, (e) => {
            me.drawLongTextBlock(me.stregoneria,e.x,e.y,e.label,e.value,e.id)
        });

        let cnt4 = me.wrap("#des4",10.5*me.step)+1;
        let cnt5 = me.wrap("#des5",10.5*me.step)+1;
        let cnt6 = me.wrap("#des6",10.5*me.step)+1;
        d3.select("#des4_rect").attr("height",lh*cnt4)
        d3.select("#des5_rect").attr("height",lh*cnt5)
        d3.select("#des6_rect").attr("height",lh*cnt6)
        d3.select("#des4_grp")
            .attr("transform","translate("+(0.25*me.step)+","+(0.5*me.step*stack_y)+")")
        d3.select("#des5_grp")
            .attr("transform","translate("+(0.25*me.step)+","+(0.5*me.step*stack_y+(cnt4+1)*lh)+")")
        d3.select("#des6_grp")
            .attr("transform","translate("+(0.25*me.step)+","+(0.5*me.step*stack_y+(cnt4+cnt5+2)*lh)+")")
        _.forEach(metrics, (e) => {
            me.drawSmallNumericBlock(me.stregoneria,e.x,e.y,e.label,e.value)
        });
        // Emplacements des charges
        _.forEach(["tm","sd","cd","ed","ld"], (e,i) => {
//             console.log(e,i)
            me.spot_g = me.stregoneria.append("g")
                .attr("id",e+"_spot_"+s.rid)
            me.spot_g.append("circle")
                .attrs({"cx":((i+1)*2.25+1)*me.step,"cy":2.75*me.step,"r":0.5*me.step})
                .styles({"fill":"#F0F0F0","stroke-width":"2pt","stroke":"#808080"})
            me.spot_g.append("text")
                .attrs({"x":((i+1)*2.25+1)*me.step-1*me.step,"y":2.5*me.step})
                .styles({"fill":"#101010","stroke":"#808080", "stroke-width":"0.5pt", "text-anchor":"start", "font-family":"4pt"})
                .text(e.toUpperCase())
        });
        let chup = 2.75
        if (s.ground_charge){
            d3.select("#tm_spot_"+s.rid).append("image")
                .attr("xlink:href", "static/main/svg/2024/tm_"+s.ground_charge+".svg" )
                .attr("width",me.step)
                .attr("height",me.step)
                .attr("x",(chup)*me.step )
                .attr("y",chup*me.step - me.step/2)
        }
        if (s.hour_charge){
            d3.select("#sd_spot_"+s.rid).append("image")
                .attr("xlink:href", "static/main/svg/2024/sd_"+s.hour_charge+".svg" )
                .attr("width",me.step)
                .attr("height",me.step)
                .attr("x",(chup+2.25)*me.step )
                .attr("y",chup*me.step - me.step/2)
        }
        if (s.consistency_charge){
            d3.select("#cd_spot_"+s.rid).append("image")
                .attr("xlink:href", "static/main/svg/2024/cd_"+s.consistency_charge+".svg" )
                .attr("width",me.step)
                .attr("height",me.step)
                .attr("x",(chup+4.5)*me.step )
                .attr("y",chup*me.step - me.step/2)
        }
        if (s.emanation_charge){
            d3.select("#ed_spot_"+s.rid).append("image")
                .attr("xlink:href", "static/main/svg/2024/ed_"+s.emanation_charge+".svg" )
                .attr("width",me.step)
                .attr("height",me.step)
                .attr("x",(chup+6.75)*me.step )
                .attr("y",chup*me.step - me.step/2)
        }
        if (s.elemental_charge){
            d3.select("#ld_spot_"+s.rid).append("image")
                .attr("xlink:href", "static/main/svg/2024/ld_"+s.elemental_charge+".svg" )
                .attr("width",me.step)
                .attr("height",me.step)
                .attr("x",(chup+9)*me.step )
                .attr("y",chup*me.step - me.step/2)
        }
        let currentdate = new Date();
        let dt = "" + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/"
                + currentdate.getFullYear() + " @ "
                + currentdate.getHours() + ":"
                + currentdate.getMinutes() + ":"
                + currentdate.getSeconds();
        me.stregoneria.append("text")
            .attrs({"x":18*me.step,"y":19*me.step})
            .styles({"font-family":"Neucha","text-anchor":"end","font-size":"12pt"})
            .text("Dragonade - Aide de jeu - Sortilège - "+s.rid+" - Edition du "+dt)
    }

    perform(code){
        super.perform();
        let me = this;
        me.init();
        me.code = code;
        me.fileprefix = "sortilege"
        me.filename = me.code
        me.drawBack();
        me.drawStregoneria();
        me.zoomActivate();
    }
}