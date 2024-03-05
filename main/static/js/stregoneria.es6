class Stregoneria extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.name = "Stregoneria";
        this.parent = "#svg_area";
    }

    init() {
        super.init();
        let me = this;
        me.version = "0.6";
        me.supertitle = "";
        me.step = 50;
        me.fontSize = 0.3*me.step + "pt";
        me.basefont = "Wellfleet";
        // Drawing Size
        me.height = me.step * 21.0
        me.width = me.step * 29.7
        me.ox = 0
        me.oy = 0

        // View Size
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));
        me.fontsize = me.step / 4 ;
        me.light = [0.70,0.4,0,0,0,0,0,0.40,0.70,0.90,1,0.90];
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
            .attr("transform", "translate(0,0)")
        ;
    }

    createPath(str,u){
        // Do not forget spaces between entities in str !!
        // Working example: str = "M 0,0 l 12,4 5,13 -5,0 -12,-17 z"
        // u is the scale unit. Try to link it to me.step
        let res = "";
        let items = str.split(" ")
        _.forEach(items, (item) => {
            if (item.includes(',')){
                let vals = item.split(',')
                res += (vals[0]*u)+","+(vals[1]*u)+" ";
            }else{
                res += item+" ";
            }
        });
        return res;
    }

    drawBack(){
        let me = this;
        me.back = me.svg.append('g')
            .attr("class","circlebacks")
            .append("g")
           // .attr("transform","translate("+(-me.step*21/2)+","+(-me.step*29.7/2)+")")
        ;
        me.back.append("rect")
            .attr("id","pagerect")
            .attr("x",me.ox*me.step)
            .attr("y",me.oy*me.step)
            .attr("width",me.width )
            .attr("height",me.height )
            .style('stroke-width','1pt')
            .style('stroke-dasharray','2 3')
            .style('stroke','#606060')
            .style('fill','#F0F0F0')
            .attr('opacity',0.5)
        ;


        me.drawPrint();

        if (me.debug == true) {
            me.xunits = 28;
            me.yunits = 20;

            let verticals = me.back.append('g')
                .attr('class', 'verticals do_not_print')
                .selectAll("g")
                .data(d3.range(1, me.xunits+2, 1));
            verticals.enter()
                .append('line')
                .attr('x1', function (d) {
                    return (d+me.ox) * me.step
                })
                .attr('x2', function (d) {
                    return (d+me.ox) * me.step
                })
                .attr('y1', me.oy*me.step)
                .attr('y2', (me.oy+me.yunits+1) * me.step)
                .style('fill', 'transparent')
                .style('stroke', '#101010')
                .style('stroke-dasharray', '3 7')
                .style('stroke-width', '0.25pt');
            let horizontals = me.back.append('g')
                .attr('class', 'horizontals do_not_print')
                .selectAll("g")
                .data(d3.range(1, me.yunits+2, 1));
            horizontals.enter()
                .append('line')
                .attr('x1', me.ox * me.step)
                .attr('x2', (me.ox+me.xunits+1) * me.step)
                .attr('y1', function (d) {
                    return (d+me.oy) * me.step
                })
                .attr('y2', function (d) {
                    return (d+me.oy) * me.step
                })
                .style('fill', 'transparent')
                .style('stroke', '#101010')
                .style('stroke-dasharray', '3 5')
                .style('stroke-width', '0.25pt');

        }
        me.back.append('text')
            .attr("x", me.step*0.5)
            .attr("y", me.step*20)
            .attr("dy", 2*me.step/3)
            .style("text-anchor","start")
            .style("font-family","Wellfleet")
            //.style("font-family","Henny Penny")
            .style("font-size",me.step/3+"pt")
            .style("fill","#101010")
            .style("stroke","#808080")
            .style("stroke-width","0.25pt")
            .text("Appartus - "+me.code)
        ;

    }

    paperX(x){
        let me = this;
        let val = me.localx + x
        val = val * me.localstep;
        return val;
    }

    paperY(y){
        let me = this;
        let val = me.localy + y;
        val = val * me.localstepy;
        return val;
    }





    drawMajorScale(tgt,x,y,scale){
        let me = this
        let sc = tgt.append('g')
            .attr('class',"scale")
        let icon = sc.append('g')
            .attr('class','icon')
            .attr('transform','translate('+x+','+y+')')
            .styles({"stroke-width":"3pt","stroke-linejoin":"round","stroke-linecap":"round"})
        icon.append('path')
            .styles({"fill":"#603060", "stroke":"#401040"})
            .attr("d","m 0,-38 l -25,5 3,45 22,27 22,-27 3,-45  z")
        icon.append('path')
            .styles({"fill":"#F0C040", "stroke":"#401040", "stroke-width":"3pt"})
            .attr("d","M 0,0 l -18,-30 l -20,20 20,20 15,-10 6,0 15,10 l 20,-20 -20,-20 -18,30 ")
        icon.append('path')
            .styles({"fill":"#401040", "stroke":"#401040"})
            .attr("d","M -30,-10 l 30,-30 30,30 -30,30 z")
        switch(scale){
            case "ge":
                icon.append('path')
                    .styles({"fill":"none", "stroke":"#F0F0F0","stroke-width":"3pt"})
                    .attr("d","M 0,0 m -10,-25 l 10,10 5,-5 -5,-5 -15,15 30,0 -15,15 -5,-5 5,-5 10,10 ");
                break;
            case "gp":
                icon.append('path')
                    .styles({"fill":"none", "stroke":"#F0F0F0","stroke-width":"3pt"})
                    .attr("d","M 0,0 m 0,0 l -10,-10 10,-10 m 0,-10 l 20,20 -20,20 -10,-10 10,-10 -10,-10 10,-10");
                break;
            case "ga":
                icon.append('path')
                    .styles({"fill":"none", "stroke":"#F0F0F0","stroke-width":"3pt"})
                    .attr("d","M 0,0 m -5,-5 l -5,5 -10,-10 20,0 10,-10 -10,-10 -10,10 10,10 20,0 -10,10 -5,-5  ");
                break;
            default:
                break;
        }
    }

    drawScale(tgt,x,y,scale){
        let me = this
        if (scale[0]=="g"){
            me.drawMajorScale(tgt,x,y,scale)
        }else{
            let sc = tgt.append('g')
                .attr('class',"scale")
            let icon = sc.append('g')
                .attr('class','icon')
                .attr('transform','translate('+x+','+y+')')
                .styles({"stroke-width":"3pt","stroke-linejoin":"round","stroke-linecap":"round"})
            icon.append('path')
                .styles({"fill":"#c08020", "stroke":"#803010"})
                .attr("d","m 0,-38 l -25,5 3,45 22,27 22,-27 3,-45 z")
            icon.append('path')
                .styles({"fill":"#401040", "stroke":"#401040"})
                .attr("d","M -30,-10 l 30,-30 30,30 -30,30 z")
            switch(scale){
                case "e":
                    icon.append('path')
                        .styles({"fill":"none", "stroke":"#F0C040","stroke-width":"3pt"})
                        .attr("d","M 0,0 m 0,-25 l -15,15 30,0 -15,15 ");
                    break;
                case "p":
                    icon.append('path')
                        .styles({"fill":"none", "stroke":"#F0C040","stroke-width":"3pt"})
                        .attr("d","M 0,0 m 0,0 l -10,-10 10,-10 m 0,-10 l 20,20 -20 20");
                    break;
                case "a":
                    icon.append('path')
                        .styles({"fill":"none", "stroke":"#F0C040","stroke-width":"3pt"})
                        .attr("d","M 0,0 m -10,0 l -10,-10 40,0 -10,10 M 0,0 m 0,-20 l -10,0 10,-10 10,10 -10,0");
                    break;
                default:
                    break;
            }
        }
    }


//     checkTextMultiline(tgt,text,width){
//         let me = this
//         let value_text_styles = {
//             "font-family":"Wellfleet",
//             "font-size":"12pt",
//             "text-anchor":"start",
//             "fill":"#101010",
//             "stroke":"#303030",
//             "stroke-width":"0.5pt",
//         }
//         d3.select("#bounds_checker")
//             .attr("id","bounds_checker")
//             .append('text')
//             .attrs({"x":0, "y":0,"dy":"0" })
//             .styles(value_text_styles)
//             .text(text)
//
//         let bbox = d3.select("#bounds_checker").getBBox()
//         if (bbox.width > me.step * width){
//             console.log("x:",bbox.x,"y:",bbox.y,"width:",bbox.width,"height:",bbox.height)
//         }
//
//     }


    drawLongTextBlock(tgt,x,y,label,value,id){
        let me = this;
        let label_attrs = {
            "width":me.step*2,
            "height":me.step*0.75,
            "rx":me.step*0.2,
            "ry":me.step*0.2
            }
        let value_attrs = {
            "width":me.step*11,
            "height":me.step*0.75,
            "rx":me.step*0.1,
            "ry":me.step*0.1
        }
        console.log("(**) ",value)
        me.drawBlock(tgt,x,y,label_attrs,value_attrs, label,value,id)
    }

    drawSmallNumericBlock(tgt,x,y,label,value,id){
        let me = this;
        let label_attrs = {
            "width":me.step*2,
            "height":me.step*0.75,
            "rx":me.step*0.2,
            "ry":me.step*0.2
            }
        let value_attrs = {
            "width":me.step*0.8,
            "height":me.step*0.75,
            "rx":me.step*0.1,
            "ry":me.step*0.1,
        }
        me.drawBlock(tgt,x,y,label_attrs,value_attrs, label,value,id)
    }

    drawBlock(tgt,x,y,label_attrs, value_attrs, label,value,id){
        let me = this;
        let label_styles = {
            "fill":"#505050",
            "stroke":"#808080",
            "stroke-width":"0pt"
        }
        let value_styles = {
            "fill":"#F0F0F0",
            "stroke":"#808080",
            "stroke-width":"1pt"
        }
        let label_text_styles = {
            "font-family":"Abel",
            "font-size":"12pt",
            "text-anchor":"middle",
            "fill":"#F0F0F0",
            "stroke":"#606060",
            "stroke-width":"0.125pt"
        }
        let value_text_styles = {
            "font-family":"Wellfleet",
            "font-size":"12pt",
            "text-anchor":"start",
            "fill":"#101010",
            "stroke":"#303030",
            "stroke-width":"0.5pt",
        }
        let grp = tgt.append('g')
            .attr("transform","translate("+x*me.step+","+y*me.step+")")
        grp.append('rect')
            .attrs({"x":0, "y":me.step*(-0.75/2) })
            .attrs(label_attrs)
            .styles(label_styles)
        grp.append('rect')
            .attr("id",id+"_rect")
            .attrs({"x":me.step*(2.1), "y":me.step*(-0.75/2) })
            .attrs(value_attrs)
            .styles(value_styles)
        grp.append('text')
            .attrs({"x":1*me.step, "y":0, "dy":"4pt" })
            .styles(label_text_styles)
            .text(label)
        grp.append('text')
            .attr("class","longwrap")
            .attr("id",id)
            .attr("x",me.step*2.25)
            .attr("y",0)
            .attr("dy","4pt")
            .style("font-family","Wellfleet")
            .style("font-size","12pt")
            .style("text-anchor","start")
            .style("fill","#101010")
            .style("stroke","#303030")
            .style("stroke-width","0.5pt")
            .text(value)
        if (me.debug == true){
            grp.append('circle')
                .attrs({"cx":0, "cy":0, "r":"3pt" })
                .styles({"fill":"red","stroke-width":0})
        }
    }

    drawStregoneria(){
        let me = this;
        let s = me.config.data[me.code].data
        let ox = 1,
            oy = 1;
        // Statistics
        me.stregoneria = me.back.append("g")
            .attr("class","stregoneria")
            .attr("id","stregoneria_"+s.rid)
            .attr("transform","translate("+ox*me.step+","+oy*me.step+")")
        ;
        me.stregoneria.append('rect')
            .attr("class","full_box")
            .attrs({"x":0, "y":-0.5*me.step,"rx":me.step*0.5,"ry":me.step*0.5,"width":me.step*14,"height":me.step*16})
            .style("fill", "#C0C0C0")
            .style("stroke", "#202020")
            .style("stroke-width", "3pt")

        me.stregoneria.append('text')
            .attrs({"x":me.step*0.25, "y":0.25*me.step})
            .styles({"font-family":"Griffy", "font-size":"24pt", "text-anchor":"start"})
            .text(s.name)

        let text_metrics = [
            {"x":0.25, "y":1, "label":"Catégorie", "value":s.category+" (Voie: "+s.path+")","id":"des1"},
            {"x":0.25, "y":2, "label":"Jet", "value":"Rêve + "+s.roll,"id":"des2"},
            {"x":0.25, "y":7, "label":"Description", "value": s.description,"id":"des4" },
        ]
        let delx = 3.5
        let metrics = [
            {"x":(delx * 0) + 0.25, "y":3, "label":"Difficulté", "value":s.diff,"id":s.rid+"met1"},
            {"x":(delx * 1) + 0.25, "y":3, "label":"Points de Rêve", "value":s.dps,"id":s.rid+"met2"},
            {"x":(delx * 2) + 0.25, "y":3, "label":"Résistance", "value":s.res,"id":s.rid+"met3"},
            {"x":(delx * 3) + 0.25, "y":3, "label":"Init", "value":s.init,"id":s.rid+"met4"},
            {"x":(delx * 0) + 0.25, "y":4, "label":"Portée", "value":s.diff,"id":s.rid+"met5"},
            {"x":(delx * 1) + 0.25, "y":4, "label":"Durée", "value":s.dps,"id":s.rid+"met6"},
            {"x":(delx * 2) + 0.25, "y":4, "label":"", "value":s.res,"id":s.rid+"met7"},
            {"x":(delx * 3) + 0.25, "y":4, "label":"", "value":s.range,"id":s.rid+"met8"},

//             {"x":5.75, "y":8, "label":"", "value":s.mastery},
//             {"x":5.75, "y":9, "label":"", "value":s.inertia},
//             {"x":5.75, "y":10, "label":"", "value":s.dps},
//             {"x":9.25, "y":8, "label":"+init", "value":s.mod_init > 0 ? "+"+a.mod_init : a.mod_init},
//             {"x":9.25, "y":9, "label":"+toucher", "value":a.mod_touch > 0 ? "+"+a.mod_touch : a.mod_touch},
//             {"x":9.25, "y":10, "label":"+dom", "value":a.mod_dmg > 0 ? "+"+a.mod_dmg : a.mod_dmg},
//             {"x":12.75, "y":8, "label":"", "value":a.mastery},
//             {"x":12.75, "y":9, "label":"", "value":a.inertia},
//             {"x":12.75, "y":10, "label":"", "value":a.dps}
        ]
        _.forEach(text_metrics, (e) => {
            me.drawLongTextBlock(me.stregoneria,e.x,e.y,e.label,e.value,e.id)
        });

        let linecount = me.wrap("#des4",10*me.step);
        d3.select("#des4_rect").attr("height",me.step*0.5*(linecount+1))

        _.forEach(metrics, (e) => {
            me.drawSmallNumericBlock(me.stregoneria,e.x,e.y,e.label,e.value)
        });
        // Emplacements Ecailles
        _.forEach([1,2,3,4,5], (e) => {
            me.stregoneria.append("circle")
                .attrs({"cx":(e*2.25+1)*me.step,"cy":5.5*me.step,"r":0.75*me.step})
                .styles({"fill":"#F0F0F0","stroke-width":"5pt","stroke":"#808080"})
            me.stregoneria.append("circle")
                .attrs({"cx":(e*2.25+1)*me.step,"cy":4.75*me.step,"r":0.3*me.step})
                .styles({"fill":"#808080","stroke":"none"})
            me.stregoneria.append('text')
                .attrs({"x":me.step*(e*2.25+1),"y":me.step*4.75, "dy":"3pt"})
                .styles({"fill":"#101010","stroke":"#404040","stroke-width":"0.5pt", "font-family":"Wellfleet", "font-size":"8pt", "text-anchor":"middle"})
                .text(e)
        });
//         // Ecailles
//         let ecailles = a.scales.split(" ")
//         _.forEach(ecailles, (v,k) => {
//             me.drawScale(me.appartus,me.step*(3+2*k), me.step*12,v);
//         })

    }

    zoomActivate() {
        let me = this;
        me.zoom = d3.zoom()
            .scaleExtent([0.25, 4])
            .on('zoom', function (event) {
                me.svg.attr('transform', event.transform)
            });
        me.vis.call(me.zoom);
    }

   register(){
//         super.register();
        let me = this;
        console.log("Register:",me.name)
        me.co.axiomaticPerformers.push(me);
    }

    perform(code){
        super.perform();
        let me = this;
        console.log("New spell code :",code)
        me.init();
        //me.debug = false
        me.code = code;

        me.drawBack();
        me.drawStregoneria();
        me.zoomActivate();
    }
}