class Risorse extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.gdr = false
        this.name = "Risorse";
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



    formatXml(xml) {
        let formatted = '';
        xml = xml.replace(/[\u00A0-\u2666]/g, function (c) {
            return '&#' + c.charCodeAt(0) + ';';
        })
        let reg = /(>)(<)(\/*)/g;
        /**/
        xml = xml.replace(reg, '$1\r\n$2$3');
        let pad = 0;
        jQuery.each(xml.split('\r\n'), function (index, node) {
            let indent = 0;
            if (node.match(/.+<\/\w[^>]*>$/)) {
                indent = 0;
            } else if (node.match(/^<\/\w/)) {
                if (pad != 0) {
                    pad -= 1;
                }
            } else if (node.match(/^<\w[^>]*[^\/]>.*$/)) {
                indent = 1;
            } else {
                indent = 0;
            }

            let padding = '';
            for (let i = 0; i < pad; i++) {
                padding += '  ';
            }

            formatted += padding + node + '\r\n';
            pad += indent;
        });

        return formatted;
    }


    saveSVG() {
        let me = this;
        me.svg.selectAll('.do_not_print').attr('opacity', 0);
        let base_svg = d3.select("#d3area svg").html();
        let flist = '<style>';
        for (let f of me.config['fontset']) {
            flist += '@import url("https://fonts.googleapis.com/css2?family=' + f + '");';
        }
        flist += '</style>';
        let lpage = "";
        let exportable_svg = '<?xml version="1.0" encoding="ISO-8859-1" ?> \
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> \
<svg class="fics_sheet" \
xmlns="http://www.w3.org/2000/svg" version="1.1" \
xmlns:xlink="http://www.w3.org/1999/xlink"> \
' + flist + base_svg + '</svg>';

        if (me.page == 0) {
            lpage = "_recto";
        } else {
            lpage = "_verso"
        }
        let fname = me.data['rid'] + lpage + ".svg"
        let nuke = document.createElement("a");
        nuke.href = 'data:application/octet-stream;base64,' + btoa(me.formatXml(exportable_svg));
        nuke.setAttribute("download", fname);
        nuke.click();
        me.svg.selectAll('.do_not_print').attr('opacity', 1);
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
//         me.back.append("rect")
//             .attr("id","pagerect")
//             .attr("x",me.ox*me.step)
//             .attr("y",me.oy*me.step)
//             .attr("width",me.width )
//             .attr("height",me.height )
//             .style('stroke-width','1pt')
//             .style('stroke-dasharray','2 3')
//             .style('stroke','#606060')
//             .style('fill','#F0F0F0')
//             .attr('opacity',0.5)
//         ;

//         if (me.debug == true) {
//             me.xunits = 28;
//             me.yunits = 20;
//
//             let verticals = me.back.append('g')
//                 .attr('class', 'verticals')
//                 .selectAll("g")
//                 .data(d3.range(1, me.xunits+2, 1));
//             verticals.enter()
//                 .append('line')
//                 .attr('x1', function (d) {
//                     return (d+me.ox) * me.step
//                 })
//                 .attr('x2', function (d) {
//                     return (d+me.ox) * me.step
//                 })
//                 .attr('y1', me.oy*me.step)
//                 .attr('y2', (me.oy+me.yunits+1) * me.step)
//                 .style('fill', 'transparent')
//                 .style('stroke', '#90a090')
//                 .style('stroke-dasharray', '3 7')
//                 .style('stroke-width', '0.25pt');
//             let horizontals = me.back.append('g')
//                 .attr('class', 'horizontals')
//                 .selectAll("g")
//                 .data(d3.range(1, me.yunits+2, 1));
//             horizontals.enter()
//                 .append('line')
//                 .attr('x1', me.ox * me.step)
//                 .attr('x2', (me.ox+me.xunits+1) * me.step)
//                 .attr('y1', function (d) {
//                     return (d+me.oy) * me.step
//                 })
//                 .attr('y2', function (d) {
//                     return (d+me.oy) * me.step
//                 })
//                 .style('fill', 'transparent')
//                 .style('stroke', '#90a090')
//                 .style('stroke-dasharray', '3 5')
//                 .style('stroke-width', '0.25pt');
//
//         }
//         me.back.append('text')
//             .attr("x", me.step*3)
//             .attr("y", me.step*21)
//             .style("text-anchor","middle")
//             .style("font-family","Are You Serious")
//             .style("font-size",me.step+"pt")
//             .style("fill","#101010")
//             .style("stroke","#808080")
//             .style("stroke-width","0.25pt")
//             .text(me.supertitle)
//         ;

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




    drawTable(tb=undefined, options){
        let me = this;
        let title = "";
        let object_values = false;
        let column_width = 1.9;
        let row_header_width = 2;
        let even_odd = false;
        let rows_header = "";
        // Dimension of the table
        let local_width = 0;
        let local_height = 0;
        let rowlen = 0;
        let collen = 0;
        let x = 0;
        let y = 0;
        let cols = [];
        let rows = [];
        let cell_width = 2;
        let cell_widths = [];
        let cell_height = 1;
        let cell_format = [];
        me.localx = me.ox + 3;
        me.localy = me.oy + 2;




    }

    rectx(d,i,rowlen,cell_width,cell_widths){
        let me = this;
        let x = 0;
        let w = 0;
        if (cell_widths.length > 0){
            while(x < i%rowlen){
                w += cell_widths[x]
                x += 1;
            }
        }
        return me.paperX(w)
    }

    recty(d,i,rowlen,cell_width,cell_widths){
        let me = this;
        return me.paperY(parseInt(i/rowlen))
    }

    wfx(d,i,rowlen,cell_width,cell_widths){
        let me = this;
        let res = 0;
        res = me.localstep*cell_width
        if (cell_widths.length > 0){
            res = me.localstep*cell_widths[i%rowlen]
        }
        return res
    }

    height(d,i,rowlen,cell_width,cell_widths){
        let me = this;
    }

    textx(d,i,rowlen,cell_width,cell_widths){
        let me = this;
        let idx = 0;
        let x = 0;
        if (cell_widths.length > 0){
            while(idx < i%rowlen){
                x += cell_widths[idx]
                idx += 1;
            }
            x += cell_widths[i%rowlen]/2;
        }
        return me.paperX(x)
    }

    texty(d,i,rowlen,cell_width,cell_widths){
        let me = this;
        return me.paperY(parseInt(i/rowlen))
    }








    zoomActivate() {
        let me = this;
        me.zoom = d3.zoom()
            .scaleExtent([0.25, 1])
            .on('zoom', function (event) {
                me.svg.attr('transform', event.transform)
            });
        me.vis.call(me.zoom);
    }

   register(){
        super.register();
        let me = this;
        me.co.globalPerformers.push(me);
    }

    drawAll(){
        let me = this;
        me.drawBack();
        let dataset = [
            {"idx": 1,"pts":2, "name":"Sanctuaire", "svg":"tm_1.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 2,"pts":2, "name":"Désert", "svg":"tm_2.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 3,"pts":2, "name":"Monts", "svg":"tm_3.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 4,"pts":2, "name":"Cité", "svg":"tm_4.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 5,"pts":2, "name":"Forêt", "svg":"tm_5.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 6,"pts":2, "name":"Plaine", "svg":"tm_6.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 7,"pts":2, "name":"Colline", "svg":"tm_7.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 8,"pts":2, "name":"Pont", "svg":"tm_8.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 9,"pts":2, "name":"Fleuve", "svg":"tm_9.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 10,"pts":2, "name":"Lac", "svg":"tm_10.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 11,"pts":2, "name":"Marais", "svg":"tm_11.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 12,"pts":2, "name":"Désolation", "svg":"tm_12.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 13,"pts":2, "name":"Gouffre", "svg":"tm_13.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},
            {"idx": 14,"pts":2, "name":"Nécropole", "svg":"tm_14.svg", "category": "Terres Médianes", "color": "#F0D080", "row":1, "hidden":1},


            {"idx": 1,"pts":4, "name":"Vaisseau", "svg":"hd_1.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 2,"pts":4, "name":"Sirène", "svg":"hd_2.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 3,"pts":4, "name":"Faucon", "svg":"hd_3.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 4,"pts":4, "name":"Couronne", "svg":"hd_4.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 5,"pts":4, "name":"Dragon", "svg":"hd_5.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 6,"pts":4, "name":"Epées", "svg":"hd_6.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 7,"pts":4, "name":"Lyre", "svg":"hd_7.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 8,"pts":4, "name":"Serpent", "svg":"hd_8.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 9,"pts":4, "name":"Poisson Acrobate", "svg":"hd_9.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 10,"pts":4, "name":"Araignée", "svg":"hd_10.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 11,"pts":4, "name":"Roseau", "svg":"hd_11.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},
            {"idx": 12,"pts":4, "name":"Chateau Dormant", "svg":"hd_12.svg", "category": "Heures Draconiques", "color": "#F0D080", "row":2, "hidden":1},


            {"idx": 1,"pts":1, "name":"Humeur", "svg":"cd_1.svg", "category": "Consistances Draconiques", "color": "#F0D080", "row":3, "hidden":1},
            {"idx": 2,"pts":1, "name":"Vapeur", "svg":"cd_2.svg", "category": "Consistances Draconiques", "color": "#F0D080", "row":3, "hidden":1},
            {"idx": 3,"pts":2, "name":"Fluide", "svg":"cd_3.svg", "category": "Consistances Draconiques", "color": "#F0D080", "row":3, "hidden":1},
            {"idx": 4,"pts":2, "name":"Précipité", "svg":"cd_4.svg", "category": "Consistances Draconiques", "color": "#F0D080", "row":3, "hidden":1},
            {"idx": 5,"pts":3, "name":"Congestion", "svg":"cd_5.svg", "category": "Consistances Draconiques", "color": "#F0D080", "row":3, "hidden":1},
            {"idx": 6,"pts":3, "name":"Amas", "svg":"cd_6.svg", "category": "Consistances Draconiques", "color": "#F0D080", "row":3, "hidden":1},
            {"idx": 7,"pts":4, "name":"Cristal", "svg":"cd_7.svg", "category": "Consistances Draconiques", "color": "#F0D080", "row":3, "hidden":1},

            {"idx": 1,"pts":1, "name":"Ondée", "svg":"em_1.svg", "category": "Emanations Draconiques", "color": "#F0D080", "row":4, "hidden":1},
            {"idx": 2,"pts":2, "name":"Flux", "svg":"em_2.svg", "category": "Emanations Draconiques", "color": "#F0D080", "row":4, "hidden":1},
            {"idx": 3,"pts":3, "name":"Courant", "svg":"em_3.svg", "category": "Emanations Draconiques", "color": "#F0D080", "row":4, "hidden":1},
            {"idx": 4,"pts":4, "name":"Vague", "svg":"em_4.svg", "category": "Emanations Draconiques", "color": "#F0D080", "row":4, "hidden":1},
            {"idx": 5,"pts":5, "name":"Marée", "svg":"em_5.svg", "category": "Emanations Draconiques", "color": "#F0D080", "row":4, "hidden":1},
            {"idx": 6,"pts":6, "name":"Ras", "svg":"em_6.svg", "category": "Emanations Draconiques", "color": "#F0D080", "row":4, "hidden":1},
            {"idx": 7,"pts":7, "name":"Déferlante", "svg":"em_7.svg", "category": "Emanations Draconiques", "color": "#F0D080", "row":4, "hidden":1},

            {"idx": 1,"pts":1, "name":"Eau", "svg":"ed_1.svg", "category": "Eléments Draconiques", "color": "#F0D080", "row":5, "hidden":1},
            {"idx": 2,"pts":1, "name":"Feu", "svg":"ed_2.svg", "category": "Eléments Draconiques", "color": "#F0D080", "row":5, "hidden":1},
            {"idx": 3,"pts":1, "name":"Terre", "svg":"ed_3.svg", "category": "Eléments Draconiques", "color": "#F0D080", "row":5, "hidden":1},
            {"idx": 4,"pts":1, "name":"Air", "svg":"ed_4.svg", "category": "Eléments Draconiques", "color": "#F0D080", "row":5, "hidden":1},
            {"idx": 5,"pts":1, "name":"Bois", "svg":"ed_5.svg", "category": "Eléments Draconiques", "color": "#F0D080", "row":5, "hidden":1},
            {"idx": 6,"pts":1, "name":"Métal", "svg":"ed_6.svg", "category": "Eléments Draconiques", "color": "#F0D080", "row":5, "hidden":1},
            {"idx": 7,"pts":1, "name":"Septième", "svg":"ed_7.svg", "category": "Eléments Draconiques", "color": "#F0D080", "row":5, "hidden":1},


            {"idx": 1,"pts":0, "name":"Conviction", "svg":"sp.svg", "category": "Spécial", "color": "#A02020", "row":6, "hidden":1},
            {"idx": 2,"pts":0, "name":"Intuition", "svg":"sp.svg", "category": "Spécial", "color": "#A02020", "row":6, "hidden":1},
            {"idx": 3,"pts":0, "name":"Révélation", "svg":"sp.svg", "category": "Spécial", "color": "#A02020", "row":6, "hidden":1},
        ]
        me.drawCardSet(dataset);
    }



    drawCardSet(set){
        let me = this;
        let cnt = set.length;
        let teta = (Math.PI*2)/(cnt);
        let radius = 20
        // Standard position
        set.forEach(function(v,k){
            if (me.gdr == true){
                v["x"] = (v["idx"]-1)*8+1;
                v["y"] = 5 + (v["row"]-1)*12;
                v["hidden"] = 0;
            }else{
               v["x"] = 10+Math.cos(teta*k)*(radius*3);
               v["y"] = 10+Math.sin(teta*k)*(radius*2);
            }
            console.log(k,v["x"],v["y"])
            v["number"] = k;
            console.log(teta)
            v["code_name"] = v["row"]+"_"+v["idx"];
            v["spot"] = 0;
        });
        me.cardset = set;
        me.drawCards();
    }




    drawCards(){
        let me = this;
        me.risorse = me.svg.append('g')
            .attr("class", "trumps")
            .selectAll("g")
            .data(me.cardset)
        ;
        me.risorsa_in = me.risorse.enter();
        me.risorsa_out = me.risorse.exit().remove();

        me.risorsa = me.risorsa_in.append('g')
            .attr("class", "trump")
            .attr("id", d => "trump__"+d["code_name"])
            .on("click", (e,d) => {

                if (e.ctrlKey){
                    d3.selectAll(".trump .verso").attr("opacity",(d) => 1);
                    d3.selectAll(".trump .recto").attr("opacity",(d) => 0)
                }else{
                    d3.selectAll(".trump .verso").attr("opacity",(d) => d['hidden'] == 1 ? 1 : 0);
                    d3.selectAll(".trump .recto").attr("opacity",(d) => d['hidden'] == 1 ? 0 : 1)
                    ;
                }
             })
            .on("mouseover", (e,d) => {
                if (e.ctrlKey){
                    console.debug(d["code_name"]+" ---> "+ "trump__"+d["code_name"] );
                }
            })
            .attr("transform", d => "translate( "+ d["x"] * me.step +","+ d["y"] * me.step + ")" )
        me.risorsa.append('rect')
                .attr('class','cardback recto')
                .attr('rx',me.step*0.5)
                .attr('ry',me.step*0.5)
                .attr('width',me.step*6)
                .attr('height',me.step*11)
                .style('fill', '#F0F0F0')
                .style('stroke', '#101010')
                .style('stroke-width', '5pt')
                ;

        me.risorsa.append("image")
                .attr('class','recto')
                .attr("xlink:href", d => "/static/main/svg/"+d["svg"] )
                .attr("width", me.step*4)
                .attr("height", me.step * 4)
                .attr("x", d => (1) * me.step)
                .attr("y", d => (3) * me.step)
                ;

        me.risorsa.append("text")
                .attr('class','recto')
                .attr("width", me.step*4)
                .attr("height", me.step * 4)
                .attr("x", d => (3.0) * me.step)
                .attr("y", d => (1.5) * me.step)
                .style("text-anchor","middle")
                .style("font-family","Are You Serious")
                .style("font-size",me.step*1.5+"pt")
                .style("fill","#101010")
                .style("stroke","#808080")
                .style("stroke-width","0.25pt")
                .text(d => d['idx'])
            ;

        me.risorsa.append("text")
                .attr('class','recto')
                .attr("width", me.step*4)
                .attr("height", me.step * 4)
                .attr("x", d => (5.75) * me.step)
                .attr("y", d => (10.5) * me.step)
                .style("text-anchor","end")
                .style("font-family","Smythe")
                .style("font-size",me.step*0.8+"pt")
                .style("fill","#a02020")
                .style("stroke","#808080")
                .style("stroke-width","0.5pt")
                .text(d => d['pts']+"r")
        me.risorsa.append("text")
                .attr('class','recto')
                .attr("x", d => (1) * me.step)
                .attr("y", d => (0.5) * me.step)
                .style("text-anchor","start")
                .style("font-family","Neucha")
                .style("font-size",me.step*0.3+"pt")
                .style("fill","#202020")
                .style("stroke","#808080")
                .style("stroke-width","0.5pt")
                .text(d => d['category'])
                .attr("transform",d => "rotate("+90+","+(0.5) * me.step+","+(0.25) * me.step+")")
              ;

        me.risorsa.append("text")
                .attr('class','recto')
                .attr("width", me.step*4)
                .attr("height", me.step * 4)
                .attr("x", d => (3) * me.step)
                .attr("y", d => (8.5) * me.step)
                .style("text-anchor","middle")
                .style("font-family","Are You Serious")
                .style("font-size",me.step*0.75+"pt")
                .style("fill","#202020")
                .style("stroke","#808080")
                .style("stroke-width","0.5pt")
                .text(d => {
                    let words = d['name'].split(' ');
                    if (words.length > 0){
                      return words[0]
                    }
                    return "";
                })


        me.risorsa.append("text")
                .attr('class','recto')
                .attr("width", me.step*4)
                .attr("height", me.step * 4)
                .attr("x", d => (3) * me.step)
                .attr("y", d => (8.5) * me.step)
                .attr("dy", me.step * 0.8)
                .style("text-anchor","middle")
                .style("font-family","Are You Serious")
                .style("font-size",me.step*0.75+"pt")
                .style("fill","#202020")
                .style("stroke","#808080")
                .style("stroke-width","0.5pt")
                .text(d => {
                    let words = d['name'].split(' ');
                    if (words.length = 2){
                      return words[1]
                    }
                    return "";
                })



        me.risorsa.append('rect')
                .attr('class','recto')
                .attr('x',d => (0.6) * me.step)
                .attr('y',d => (0.5) * me.step)
                .attr('width',me.step*0.25)
                .attr('height',me.step*10)
                .style('fill', d => d["color"])
                .style('fill-opacity', 0.80)
                .style('stroke', '#808080')
                .style('stroke-width', '1pt')
                ;

        me.risorsa.append('rect')
                .attr('class','cardback verso')
                .attr('rx',me.step*0.5)
                .attr('ry',me.step*0.5)
                .attr('width',me.step*6)
                .attr('height',me.step*11)
                .style('fill', '#102030')
                .style('stroke', '#909090')
                .style('stroke-width', '5pt')
                .attr("opacity", d => d["hidden"])
        ;

        me.risorsa.append("image")
                .attr('class','verso')
                .attr("xlink:href", "/static/main/svg/dragonade_logo.svg")
                .attr("width", me.step*5)
                .attr("height", me.step* 8)
                 .attr("x", d => 0.5 * me.step)
                 .attr("y", d => 1 * me.step)
                .attr("opacity", d => d["hidden"])
        ;

        me.drawCross(0,10*me.step)
        me.drawCross(10*me.step,0)
    }

    refreshSelection(code_name){
        let me = this;
        if (me.selection.includes(code_name)){
            me.selection.pop(code_name);
        }else{
            me.selection.push(code_name);
        }
        if (me.selection.length >= 5){
            me.doReveal();
        }
    }

    doReveal(){
        let me = this;
        let c = 0
        d3.selectAll(".trump .recto").attr("opacity",0);
        d3.selectAll(".trump .verso").attr("opacity",0);
        console.log(me.selection)
        me.selection.forEach( v => {
            console.log(v)
            d3.selectAll("#trump__"+v)
                .attr("transform", d => "translate( "+ (70+c*8) * me.step +","+ (53 * me.step) + ")" )
            d3.selectAll("#trump__"+v+" .verso")
                .attr("opacity",1.0);
            c+=1;
        });
        me.revealling = true;
    }


    updateCards(){
       let me = this;
       //me.risorsa_update = me.risorse.update();
       d3.selectAll(".trump .verso").attr("opacity",(d) => 1);
       d3.selectAll(".trump .recto").attr("opacity",(d) => 0)
       d3.selectAll(".trump")
            .transition()
            .duration(2000)
            .ease(d3.easeCubicInOut)
            .attr("transform", d => "translate( "+ d["x"] * me.step +","+ d["y"] * me.step + ")")
            .delay(250)
            ;

    }





    action(type,str){
        let me = this;
        if (me.gdr == false){
            let cards = str.split(" ");
            let row = 1
            let col = 1
            let cnt = me.cardset.length;
            let colhidden = 1 + Math.floor(Math.random()*cnt) % cnt;
            let teta = (Math.PI*2)/(cnt - cards.length);
            let radius = 20
            console.log("Type:",type)
            if (type==="select"){
                _.map(me.cardset, (c) => {
                    let rowstr = `${row}`;
                    if (cards[`${row-1}`] == "0"){
                        row += 1
                    }else{
                        if ((c["row"] == rowstr) && (c["idx"] == cards[`${row-1}`])){
                            c["hidden"] = 0
                            c["x"] = (col-1)*8-5;
                            c["y"] = 0 + (1)*12;
                            row += 1
                            col += 1
                            console.log("=> ",rowstr,cards[row],c["row"],c["idx"])
                        }else{
                            c["hidden"] = 1
                            c["x"] = 10+Math.cos(teta*colhidden)*(radius*3);
                            c["y"] = 10+Math.sin(teta*colhidden)*(radius*2);
                            colhidden += 1
                        }
                    }
                });
                me.updateCards();

            }else{
                console.log("I'm here!!")
                d3.selectAll(".trump .verso")
                    .attr("opacity",(d) => {
                        let val = 0.0
                        if (d['hidden'] == 1){
                            console.log("verso:", d.name, "is visible");
                            val = 1.0
                        }
                        return val;
                    });
                d3.selectAll(".trump .recto")
                    .attr("opacity",(d) => {
                        let val = 0.0
                        if (d['hidden'] == 0){
                            console.log("recto:", d.name, "is visible");
                            val = 1.0
                        }
                        return val;
                    });
            }
        }
    }

    perform(){
        super.perform();
        let me = this;
        console.log(me.name+" PERFORMING!!! ")
        me.init();
        console.log(me.name)
        me.drawAll();
        me.zoomActivate();
    }
}