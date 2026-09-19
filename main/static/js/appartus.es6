class Appartus extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.name = "Appartus";
        this.parent = "#svg_area";
    }

    init() {
        super.init();
        let me = this;
        me.version = "0.7";
        me.supertitle = "";
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



    drawAppartus(){
        let me = this;
        let a = me.datum.payload
        let ox = 0.5, oy = 1.5
        // Statistics
        me.appartus = me.back.append("g")
            .attr("class","artefatto")
            .attr("id","artefatto_"+a.rid)
            .attr("transform","translate("+ox*me.step+","+oy*me.step+")")
        me.appartus.append('rect')
            .attr("class","rect_top")
            .attrs({"x":0*me.step, "y":me.step*0,"rx":me.step*0.1,"ry":me.step*0.1,"width":me.step*(29.7/2-1.75),"height":me.step*3.0})
            .style("fill", "#ffffff")
            .style("stroke", "black")
            .style("stroke-width", "1pt")
        me.appartus.append('rect')
            .attr("class","rect_bottom")
            .attr("id","rectbot")
            .attrs({"x":0, "y":me.step*3.25,"rx":me.step*0.1,"ry":me.step*0.1,"width":(me.step*(29.7/2-1.75)),"height":me.step*13.25})
            .style("fill", "#ffffff")
            .style("stroke", "black")
            .style("stroke-width", "1pt")
        me.appartus.append('text')
            .attrs({"x":me.step*0.25, "y":(-0.25)*me.step})
            .styles({"font-family":me.titleFont, "font-size":me.fontSize*4+"pt", "text-anchor":"start"})
            .text(a.name)
        me.appartus.append('text')
            .attrs({"x":me.step*13.75, "y":-0.25*me.step})
            .styles({"font-family":"Wellfleet", "font-size":me.fontSize*4+"pt", "text-anchor":"end"})
            .text(a.puissance)
        let stack_y = 11
        let text_metrics = [
            {"x":0.25, "y":0.5, "label":"Apparence", "value":a.glance, "id":"att1"},
            {"x":0.25, "y":1, "label":"Possesseur", "value":a.owner, "id":"att2"},
            {"x":0.25, "y":1.5, "label":"Matériaux", "value":a.materials, "id":"att3"},
            {"x":0.25, "y":2, "label":"Catégorie", "value":a.category+" ("+a.type+")", "id":"att4"},
            {"x":0.25, "y":stack_y, "label":"Creator", "value":a.creator, "id":"att5"},
            {"x":0.25, "y":stack_y, "label":"Description", "value":a.description, "id":"att6"},
            {"x":0.25, "y":stack_y, "label":"Utilisation", "value":a.rules, "id":"att7"},
            {"x":0.25, "y":stack_y, "label":"Notes", "value":a.notes, "id":"att8"}
        ]
        let metrics = [
            {"x":0.25, "y":2.5, "label":"Maîtrise", "value":a.mastery, "id":"met1"},
            {"x":0.25, "y":3, "label":"Inertie", "value":a.inertia, "id":"met2"},
            {"x":0.25, "y":3.5, "label":"Points de Rêve", "value":a.dps, "id":"met3"},
            {"x":3.25, "y":2.5, "label":"Charges", "value":a.charges, "id":"met4"},
            {"x":3.25, "y":3, "label":"", "value":"", "id":"met5"},
            {"x":3.25, "y":3.5, "label":"", "value":"", "id":"met6"},
            {"x":6.25, "y":2.5, "label":"", "value":"", "id":"met7"},
            {"x":6.25, "y":3, "label":"", "value":"", "id":"met8"},
            {"x":6.25, "y":3.5, "label":"", "value":"", "id":"met9"},
            {"x":9.25, "y":2.5, "label":"+init", "value":a.mod_init > 0 ? "+"+a.mod_init : a.mod_init, "id":"met10"},
            {"x":9.25, "y":3, "label":"+toucher", "value":a.mod_touch > 0 ? "+"+a.mod_touch : a.mod_touch, "id":"met11"},
            {"x":9.25, "y":3.5, "label":"+dom", "value":a.mod_dmg > 0 ? "+"+a.mod_dmg : a.mod_dmg, "id":"met12"}
        ]
        _.forEach(text_metrics, (e) => {
            me.drawLongTextBlock(me.appartus,e.x,e.y,e.label,e.value,e.id)
        });
        _.forEach(metrics, (e) => {
            me.drawSmallNumericBlock(me.appartus,e.x,e.y,e.label,e.value,e.id)
        });
        // Emplacements des écailles
        _.forEach([1,2,3,4,5,6,7], (e) => {
            let offset_x = (e*1.5-0.5)*me.step
            me.appartus.append("circle")
                .attrs({"cx": offset_x,"cy":4.65*me.step,"r":0.6*me.step})
                .styles({"fill":"#F0F0F0","stroke-width":"5pt","stroke":"#808080"})
            me.appartus.append("circle")
                .attrs({"cx":offset_x,"cy":3.9*me.step,"r":0.2*me.step})
                .styles({"fill":"#808080","stroke":"none"})
            me.appartus.append('text')
                .attrs({"x":offset_x,"y":me.step*3.9, "dy":"3pt"})
                .styles({"fill":"#101010","stroke":"#404040","stroke-width":"0.5pt", "font-family":"Wellfleet", "font-size":"8pt", "text-anchor":"middle"})
                .text(e)
        });
        // Ecailles
        let ecailles = a.scales.split(" ")
        _.forEach(ecailles, (v,k) => {
            let offset_x = ((k+1)*1.5-0.5)*me.step
            me.drawScale(me.appartus,offset_x, me.step*4.70,v);
        })
        let cnt5 = me.wrap("#att5",10.5*me.step)+1;
        let cnt6 = me.wrap("#att6",10.5*me.step)+1;
        let cnt7 = me.wrap("#att7",10.5*me.step)+1;
        let cnt8 = me.wrap("#att8",10.5*me.step)+1;
        let lh = 0.425*2/3*me.step
        d3.select("#att5_rect").attr("height",cnt5*lh)
        d3.select("#att6_rect").attr("height",cnt6*lh)
        d3.select("#att7_rect").attr("height",cnt7*lh)
        d3.select("#att8_rect").attr("height",cnt8*lh)
        d3.select("#att5_grp")
            .attr("transform","translate("+(0.25*me.step)+","+((0.5*me.step*stack_y))+")")
        d3.select("#att6_grp")
            .attr("transform","translate("+(0.25*me.step)+","+((0.5*me.step*stack_y)+((cnt5+1)*lh))+")")
        d3.select("#att7_grp")
            .attr("transform","translate("+(0.25*me.step)+","+((0.5*me.step*stack_y)+(cnt5+cnt6+2)*lh)+")")
        d3.select("#att8_grp")
            .attr("transform","translate("+(0.25*me.step)+","+((0.5*me.step*stack_y)+(cnt5+cnt6+cnt7+3)*lh)+")")
        d3.select("#rectbot").attr("height",(cnt5+cnt6+cnt7+cnt8+3+4)*lh)
        let currentdate = new Date();
        let dt = "" + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/"
                + currentdate.getFullYear() + " @ "
                + currentdate.getHours() + ":"
                + currentdate.getMinutes() + ":"
                + currentdate.getSeconds();
        me.appartus.append("text")
            .attrs({"x":18*me.step,"y":19*me.step})
            .styles({"font-family":"Neucha","text-anchor":"end","font-size":"12pt"})
            .text("Dragonade - Aide de jeu - Appartus - "+a.rid+" - Edition du "+dt)
    }

    drawScale(tgt,x,y,scale){
        let me = this
        let sc = tgt.append('g')
            .attr('class',"scale")
        let icon = sc.append('g')
            .attr('class','icon')
            .attr('transform','translate('+(x)+','+(y)+')')
        icon.append("image")
            .attr('transform','translate('+(-33)+','+(-36)+')')
            .attr("xlink:href", "static/main/svg/2026/"+scale+".svg" )
            .style('width',(me.step)+"pt")
        icon.append("circle")
            .attr("r","1pt")
            .styles({"stroke-width":"1pt","stroke":"none","fill":"red"})
    }

    perform(code){
        super.perform();
        let me = this;
        me.init();
        me.code = code;
        me.fileprefix = "artefact"
        me.filename = me.code
        me.drawBack();
        me.drawAppartus();
        me.zoomActivate();
    }

    postFetch(){
        super.postFetch()
        let me = this
        console.log("POST FETCH APPARTUS")
        console.log(me.datum)
        console.log(`${me.code} ${me.name}`)
        me.fetched = true
        me.drawBack()
        me.drawAppartus()
        me.zoomActivate()
    }

    goBack(){
        super.goBack()
        $("#svg_area").remove()
    }

    handle(code){
        super.handle()
        let me = this
        me.code = code
        me.fileprefix = "artefatto"
        me.filename = me.code
        $("<div id='svg_area'></div>").insertBefore('.zlist_container')
        me.init()
        me.fetch("artefatto",code)

    }


}