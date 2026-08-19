class Stregoneria extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.name = "Stregoneria"
        this.parent = "#svg_area"
        this.fetched = false
        console.log(config)
    }

    init() {
        super.init();
        let me = this;
        me.version = "1.0.0";
        me.supertitle = "";
        me.category = "stregoneria"

        me.fontSize = 10 //me.step / 6
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

    drawStregoneria(){
        let me = this;
        let s = {}
        me.klass = "Stregoneria"
        // me.rid = s.rid
        console.log("DRAW STREGONERIA")
        // if (me.fetched == true) {
        //     _.forEach(me.config.data, (v, k) => {
        //         if (v.rid == me.code) {
        //             s = v
        //             return false
        //         }
        //     })
        // }else{
        //     console.log("DATUM FETCHED!!!")
        s = me.datum.payload
        // }
        console.log(s)
        let ox = 0.5, oy = 1.5
        // Statistics
        me.stregoneria = me.back.append("g")
            .attr("class","stregoneria")
            .attr("id","stregoneria_"+s.rid)
            .attr("transform","translate("+ox*me.step+","+oy*me.step+")")
        me.stregoneria.append('rect')
            .attr("class","rect_top")
            .attrs({"x":0*me.step, "y":me.step*0,"rx":me.step*0.1,"ry":me.step*0.1,"width":me.step*(29.7/2-1.75),"height":me.step*3.0})
            .style("fill", "#ffffff")
            .style("stroke", "black")
            .style("stroke-width", "1pt")
        me.stregoneria.append('rect')
            .attr("class","rect_bottom")
            .attr("id","rectbot")
            .attrs({"x":0, "y":me.step*3.25,"rx":me.step*0.1,"ry":me.step*0.1,"width":(me.step*(29.7/2-1.75)),"height":me.step*13.25})
            .style("fill", "#ffffff")
            .style("stroke", "black")
            .style("stroke-width", "1pt")
        me.stregoneria.append('text')
            .attrs({"x":me.step*0.25, "y":(-0.25)*me.step})
            .styles({"font-family":me.titleFont, "font-size":me.fontSize*4+"pt", "text-anchor":"start"})
            .text(s.name)

        let lh = 0.5*2/3*me.step
        let stack_y = 7.5
        let text_metrics = [
            // {"x":0.25, "y":0.5, "label":"Catégorie", "value":s.category+" (Voie: "+s.path+")","id":"des1", edit_field: ""},
            {"x":0.25, "y":0.5, "label":"Jet", "value":"Rêve + "+s.roll,"id":"des2", edit_field: "" },
            {"x":0.25, "y":stack_y, "label":"Description", "value": s.description,"id":"des4", edit_field: "description" },
            {"x":0.25, "y":stack_y, "label":"Notes", "value": s.composantes,"id":"des5", edit_field: "composantes" },
            // {"x":0.25, "y":stack_y, "label":"Autres noms", "value": s.alternative_names,"id":"des6", edit_field: "alternative_names" },
        ]
        let delx = 4
        let metrics = [
            {"x":(delx * 0) + 0.25, "y":1.5, "label":"Difficulté", "value":s.diff,"id":s.rid+"met1"},
            {"x":(delx * 0) + 0.25, "y":2.0, "label":"PdR", "value":s.dps,"id":s.rid+"met2"},
            {"x":(delx * 0) + 0.25, "y":2.5, "label":"Durée", "value":s.duration_str,"id":s.rid+"met3"},

            {"x":(delx * 1) + 0.25, "y":1.5, "label":"Résistance", "value":s.resistance,"id":s.rid+"met4"},
            {"x":(delx * 1) + 0.25, "y":2.0, "label":"Temps Incant.", "value":s.ti_str,"id":s.rid+"met5"},
            {"x":(delx * 1) + 0.25, "y":2.5, "label":"Zone/Taille", "value":s.area_str,"id":s.rid+"met6"},

            {"x":(delx * 2) + 0.25, "y":1.5, "label":"Portée", "value":s.range_str,"id":s.rid+"met7"},
            {"x":(delx * 2) + 0.25, "y":2.0, "label":"Coût en Songe", "value":s.songe,"id":s.rid+"met8"},

            // {"x":(delx * 1) + 0.25, "y":2.5, "label":"", "value":"","id":s.rid+"met8"},
        ]
        _.forEach(text_metrics, (e) => {
            me.drawLongTextBlock(me.stregoneria,e.x,e.y,e.label,e.value,e.id,e.edit_field)
        });

        let cnt4 = me.superwrap("#des4",9*me.step)+1;
        let cnt5 = me.superwrap("#des5",9*me.step)+1;
        // let cnt6 = me.superwrap("#des6",8*me.step)+1;
        d3.select("#des4_rect").attr("height",lh*cnt4)
        d3.select("#des5_rect").attr("height",lh*cnt5)
        // d3.select("#des6_rect").attr("height",lh*cnt6)
        d3.select("#des4_grp")
            .attr("transform","translate("+(0.25*me.step)+","+(0.5*me.step*stack_y)+")")
        d3.select("#des5_grp")
            .attr("transform","translate("+(0.25*me.step)+","+(0.5*me.step*stack_y+(cnt4+1)*lh)+")")
        // d3.select("#des6_grp")
        //     .attr("transform","translate("+(0.25*me.step)+","+(0.5*me.step*stack_y+(cnt4+cnt5+2)*lh)+")")
        _.forEach(metrics, (e) => {
            me.drawSmallNumericBlock(me.stregoneria,e.x,e.y,e.label,e.value)
        });
        // Emplacements des charges
        let basex = 0.5
        let basey = 15.5
        let chup = 2.5
        _.forEach([
            {"code":"tm","name":"terre","charge":"ground_charge"},
            {"code":"sd","name":"signe","charge":"hour_charge"},
            {"code":"cd","name":"consistance","charge":"consistency_charge"},
            {"code":"ed","name":"emanation","charge":"emanation_charge"},
            {"code":"ld","name":"élément","charge":"elemental_charge"},
            ], (e,i) => {
            me.spot_g = me.stregoneria.append("g")
                .attr("id",e.code+"_spot_"+s.rid)
            me.spot_g.append("circle")
                .attrs({"cx":(basex+1+(i*2.5))*me.step,"cy":(basey+0.9)*me.step,"r":1.2*me.step})
                .styles({"fill":"white","stroke-width":"3pt","stroke":"black","stroke-dasharray":"1 3"})
            me.spot_g.append("text")
                .attrs({"x":(basex+1+(i*2.5))*me.step,"y":(basey+2.5)*me.step})
                .styles({"fill":"black","stroke":"black", "stroke-width":"0.5pt", "text-anchor":"middle", "font-family":me.baseFont, "font-size":"8pt"})
                .text(e.name.toUpperCase())
            if (s[e.charge]){
                d3.select("#"+e.code+"_spot_"+s.rid).append("image")
                    .attr("class","relinkable")
                    .attr("xlink:href", "static/main/svg/2026/"+e.code+"_"+s[e.charge]+".svg" )
                    .attr("width",me.step*2)
                    .attr("height",me.step*2)
                    .attr("x",(basex+(i*2.5))*me.step)
                    .attr("y",(basey-0.25)*me.step )
            }
        });
        // Catégorie
        me.spot_g = me.stregoneria.append("g")
                .attr("id","category_spot_"+s.rid)
        me.spot_g.append("circle")
                .attrs({"cx":(basex+12.5)*me.step,"cy":(basey-3)*me.step,"r":1*me.step})
                .styles({"fill":"#F0F0F0","stroke-width":"0pt","stroke-dasharray":"1 4","stroke":"#000000"})
        d3.select("#category_spot_"+s.rid).append("image")
            .attr("class","relinkable")
            .attr("xlink:href", "static/main/svg/2026/"+s.category.toLowerCase()+".svg" )
            .attr("width",me.step*2)
            .attr("height",me.step*2)
            .attr("x",(basex+11.5)*me.step)
            .attr("y",(basey-4)*me.step )
        // VOIE
        let cat = s.path.toLowerCase()
        if (cat[0]=='g'){
            cat = "generique"
        }
        console.log(cat)
        me.spot_g.append("circle")
                .attrs({"cx":(basex+12.5)*me.step,"cy":(basey-1)*me.step,"r":1*me.step})
                .styles({"fill":"#F0F0F0","stroke-width":"0pt","stroke-dasharray":"1 4","stroke":"black"})
        d3.select("#category_spot_"+s.rid).append("image")
            .attr("class","relinkable")
            .attr("xlink:href", "static/main/svg/2026/"+cat+".svg" )
            .attr("width",me.step*2)
            .attr("height",me.step*2)
            .attr("x",(basex+11.5)*me.step)
            .attr("y",(basey-2)*me.step )
        // Puissance
        me.spot_g.append("circle")
                .attrs({"cx":(basex+12.5)*me.step,"cy":(basey-15.5)*me.step,"r":0.5*me.step})
                .styles({"fill":"white","stroke-width":"2pt","stroke-dasharray":"","stroke":"black"})
        me.stregoneria.append('text')
            .attrs({"x":(basex+12.5)*me.step,"y":(basey-15.4)*me.step})
            .styles({"font-family":me.altFont, "font-size":me.fontSize*2+"pt", "text-anchor":"middle"})
            .text(s.puissance)

        // Signature
        me.dragonadeSignature(.75,20,s.rid,"Fiche de Sortilège: "+s.name)
    }


    perform(code){
        super.perform();
        let me = this;
        me.init();
        me.code = code;
        me.fileprefix = "sortilege"
        me.filename = me.code
        me.drawBack()
        me.drawStregoneria()
        me.zoomActivate()
    }

    postFetch(){
        super.postFetch()
        let me = this
        console.log("POST FETCH STREGONERIA")
        console.log(me.datum)
        console.log(`${me.code} ${me.name}`)
        me.fetched = true
        me.drawBack()
        me.drawStregoneria()
        me.zoomActivate()
    }

    goBack(){
        super.goBack()
        // $(".zlist_container").css('display','flex')
        $("#svg_area").remove()
    }

    handle(code){
        console.log()
        super.handle()
        let me = this
        me.code = code
        me.fileprefix = "incantessimo"
        me.filename = me.code
        // $(".zlist_container").css('display','none')
        $("<div id='svg_area'></div>").insertBefore('.zlist_container')
        me.init()
        me.fetch("incantessimo",code)

    }

}