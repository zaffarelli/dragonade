class Carte extends Modulo {
    constructor(co,config) {
        super(co,config);
        this.name = "Carte";
        this.parent = "#svg_area";
        console.log('Carte Constructor')
    }

    init() {
        super.init();
        let me = this;
        me.version = "0.6";
        me.supertitle = "";
        me.step = 50;
        me.fontSize = 0.3*me.step + "pt";
        // Drawing Size
        me.height = me.step * 21.0
        me.width = me.step * 29.7
        me.ox = 0.85
        me.oy = 0.5
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

        if (me.debug == true) {
            me.xunits = 28;
            me.yunits = 20;

            let verticals = me.back.append('g')
                .attr('class', 'verticals')
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
                .style('stroke', '#90a090')
                .style('stroke-dasharray', '3 7')
                .style('stroke-width', '0.25pt');
            let horizontals = me.back.append('g')
                .attr('class', 'horizontals')
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
                .style('stroke', '#90a090')
                .style('stroke-dasharray', '3 5')
                .style('stroke-width', '0.25pt');

        }
        me.back.append('text')
            .attr("x", me.step*3)
            .attr("y", me.step*21)
            .style("text-anchor","middle")
            .style("font-family","Are You Serious")
            .style("font-size",me.step+"pt")
            .style("fill","#101010")
            .style("stroke","#808080")
            .style("stroke-width","0.25pt")
            .text(me.supertitle)
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




    drawTable(src, options){
        let me = this;
        console.log(src)
        let tb = JSON.parse(src["data"]);
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


        console.log(tb)
        console.log("---")
        console.log(tb["data"])
        console.log("===")



        if (tb){
            if ("title" in tb){
                title = tb["title"]
            }
            if ("options" in tb){
                if ("column_width" in tb["options"]){
                    column_width = tb["options"]["column_width"];
                }
                if ("object_values" in tb["options"]){
                    object_values = tb["options"]["object_values"];
                }
                if ("rows_header" in tb["options"]){
                   rows_header = tb["options"]["rows_header"];
                }
                if ("row_header_width" in tb["options"]){
                    row_header_width = tb["options"]["row_header_width"];
                }
                if ("even_odd" in tb["options"]){
                    even_odd = tb["options"]["even_odd"];
                }
                if ("cell_width" in tb["options"]){
                    cell_width = tb["options"]["cell_width"];
                }
                if ("cell_widths" in tb["options"]){
                    cell_widths = tb["options"]["cell_widths"];
                }
                if ("cell_format" in tb["options"]){
                    cell_format = tb["options"]["cell_format"];
                }
                if ("cell_height" in tb["options"]){
                    cell_height = tb["options"]["cell_height"];
                }
            }
            if ("cols" in tb){
                rowlen = tb["cols"].length;
                cols = tb["cols"]
            }
            if ("rows" in tb){
                collen = tb["rows"].length;
                rows = tb["rows"]
            }
            if ("x" in options){
                x = options["x"];
                me.localx += options["x"];
            }
            if ("y" in options){
                y = options["y"];
                me.localy += options["y"];
            }

        }
        let table = me.back.append('g').attr('id',title)
            .attr("transform","translate("+(me.step*0.5)+","+(me.step*1)+")")
        me.localstep = me.step/2;
        me.localstepy = me.step/2*cell_height;
        me.localfontSize = 0.3*me.localstep;
        let columns = table.append('g')
            .attr('class','table_columns')
            .selectAll('.table_col')
            .data(cols)
        let cols_in = columns.enter();
        let cols_out = columns.exit().remove();
        let col = cols_in.append('g').attr('class','table_col');
        col.append('rect')
            .attr("x", (d,i) => {
                let w = (i%rowlen)*cell_width;
                if (cell_widths.length > 0){
                    x = 0;
                    w = 0;
                    while(x < i%rowlen){
                        w += cell_widths[x]
                        x += 1;
                    }
                }
                return me.paperX(w)
            })
            .attr("y", (d,i) => me.paperY(-1))
            .attr("rx", me.localstep/8)
            .attr("ry", me.localstep/8)
            .attr("width",(d,i) => {
                let res = 0;
                if (object_values){
                    res = me.localstep*d["width"]*3
                }else {
                    res = me.localstep*cell_width
                    if (cell_widths.length > 0){
                        res = me.localstep*cell_widths[i%rowlen]
                        console.log(res)
                    }
                }
                return res
            })
            .attr("height",me.localstep*cell_height)
            .attr("stroke","#C0C0C0")
            .attr("stroke-width","0.5pt")
            .style("fill","#F0F0F0")
        ;
        col.append('text')
            .attr("y", (d,i) => me.paperY(-0.75))
            .attr("x", (d,i) => me.textx(d,i,rowlen,cell_width,cell_widths))
            .attr("dy",me.localfontSize*cell_height)
            .style("text-anchor","middle")
            .style("font-family","Neucha")
            .style("font-size",me.localfontSize+"pt")
            .style("fill","#101010")
            .style("stroke","#808080")
            .style("stroke-width","0.25pt")
            .text((d,i) => d)
        ;

        if ("col_back_header" in tb){
            let cbhs = table.append('g')
                .attr('class','table_columns')
                .selectAll('.table_colbh')
                .data(tb['col_back_header'])
            let cbh_in = cbhs.enter();
            let cbh_out = cbhs.exit().remove();
            let cbh = cbh_in.append('g').attr('class','table_colbh');
            cbh.append('rect')
                .attr("x", (d,i) => me.paperX((i%rowlen)*2))
                .attr("y", (d,i) => me.paperY(collen))
                .attr("rx", me.localstep/4)
                .attr("ry", me.localstep/4)
                .attr("width",(d,i) => {
                    let res = 0;
                    if (object_values){
                        res = me.localstep*d["width"]*3
                    }else {
                        res = me.localstep*cell_width
                        if (cell_widths.length > 0){
                            res = me.localstep*cell_widths[i%rowlen]
                            console.log(res)
                        }
                    }
                    return res
                })
                .attr("height",me.localstep*0.8)
                .attr("stroke","#606060")
                .attr("stroke-width","0.5pt")
                .style("fill","#F0F0F0")
            ;
            cbh.append('text')
                .attr("x", (d,i) => me.paperX((i%rowlen)*2+1))
                .attr("y", (d,i) => me.paperY(collen+1-0.5))
                .style("text-anchor","middle")
                .style("font-family","Neucha")
                .style("font-size",me.localfontSize+"pt")
                .style("fill","#101010")
                .style("stroke","#808080")
                .style("stroke-width","0.25pt")
                .text((d,i) => d)
            ;
        }

        if ("row_back_header" in tb){
            let rbhs = table.append('g')
                .attr('class','table_columns')
                .selectAll('.table_rowbh')
                .data(tb['row_back_header'])
            let rbh_in = rbhs.enter();
            let rbh_out = rbhs.exit().remove();
            let rbh = rbh_in.append('g').attr('class','table_rowbh');
            rbh.append('rect')
                .attr("x", (d,i) => me.paperX((rowlen)*2))
                .attr("y", (d,i) => me.paperY(i))
                .attr("rx", me.localstep/4)
                .attr("ry", me.localstep/4)
                .attr("width",me.localstep*1.9)
                .attr("height",me.localstep*0.8)
                .attr("stroke","#606060")
                .attr("stroke-width","0.5pt")
                .style("fill","#F0F0F0")
            ;
            rbh.append('text')
                .attr("x", (d,i) => me.paperX((rowlen)*2+1))
                .attr("y", (d,i) => me.paperY(i+0.5))
                .style("text-anchor","middle")
                .style("font-family","Neucha")
                .style("font-size",me.localfontSize+"pt")
                .style("fill","#101010")
                .style("stroke","#808080")
                .style("stroke-width","0.25pt")
                .text((d,i) => d)
            ;
        }


        if (rows_header != ""){
            let k = table.append('g');
            k.append('rect')
                .attr("x", (d,i) => me.paperX(-1*row_header_width)+2)
                .attr("y", (d,i) => me.paperY(-1))
                .attr("rx", me.localstep/8)
                .attr("ry", me.localstep/8)
                .attr("width",me.localstep*row_header_width*0.95)
                .attr("height",me.localstep*cell_height)
                .attr("stroke","#C0C0C0")
                .attr("stroke-width","0.5pt")
                .style("fill","#F0F0F0")
            ;
            k.append('text')
                .attr("x", (d,i) => me.paperX(-1))
                .attr("y", (d,i) => me.paperY(0-0.4))
                .style("text-anchor","middle")
                .style("font-family","Neucha")
                .style("font-size",me.localfontSize+"pt")
                .style("fill","#101010")
                .style("stroke","#808080")
                .style("stroke-width","0.25pt")
                .text((d,i) => rows_header)
            ;
        }

        let rowxs = table.append('g')
            .attr('class','table_rows')
            .selectAll('.table_row')
            .data(tb['rows'])
        let rows_in = rowxs.enter();
        let rows_out = rowxs.exit().remove();
        let row = rows_in.append('g').attr('class','table_row');
        row.append('rect')
            .attr("x", (d,i) => me.paperX(-1*row_header_width)+2)
            .attr("y", (d,i) => me.paperY(i))

            .attr("rx", me.localstep/8)
            .attr("ry", me.localstep/8)
            .attr("width", (d,i) => {
                let result = me.localstep*row_header_width*0.95
                return result
            })
            .attr("height",me.localstep*cell_height)
            .attr("stroke","#C0C0C0")
            .attr("stroke-width","0.5pt")
            .attr("fill", (d,i) => {
                let color = "#F0F0F0";
//                 if (even_odd){
//                     if (i%2==0){
//                         color = "#FFFFFF";
//                     }else{
//                         color = "#EEEEFE";
//                     }
//                 }
                return color;
            })
        ;
        row.append('text')
            .attr("x", (d,i) => me.paperX(-1*row_header_width+row_header_width/2))
            //.attr("y", (d,i) => me.paperY(i+0.5))
            .attr("y", (d,i) => me.texty(d,i,1,cell_width,cell_widths))
            .attr("dy",me.localfontSize*1.2)
            .style("text-anchor","middle")
            .style("font-family","Neucha")
            .style("font-size",me.localfontSize+"pt")
            .style("fill","#101010")
            .style("stroke","#808080")
            .style("stroke-width","0.25pt")
            .text((d,i) => d)
        ;


        let cells = table.append('g')
            .attr('class','table_cells')
            .selectAll('.table_cell')
            .data(tb['values'])
        let cells_in = cells.enter();
        let cells_out = cells.exit().remove();
        let cell = cells_in.append('g').attr("id", (d,i) => i).attr('class','table_cell');
        cell.append('rect')
            .attr("x", (d,i) => me.rectx(d,i,rowlen,cell_width,cell_widths))
            .attr("y", (d,i) => me.recty(d,i,rowlen,cell_width,cell_widths))
            .attr("width",(d,i) => me.wfx(d,i,rowlen,cell_width,cell_widths))
            .attr("height",me.localstep*cell_height)
            .attr("fill", (d,i) => {
                let color = "#FFFFFF";
                if (even_odd){
                    if (parseInt(i/rowlen)%2==0){
                        color = "#FFFFFF";
                    }else{
                        color = "#EEEEFE";
                    }
                }
                if (object_values){
                    color = d["color"];
                }
                return color;
            })
            .attr("stroke","#C0C0C0")
            .attr("stroke-width","0.5pt")
        ;
        cell.append('text')
            .attr("x", (d,i) => me.textx(d,i,rowlen,cell_width,cell_widths))
            .attr("y", (d,i) => me.texty(d,i,rowlen,cell_width,cell_widths))
            .attr("dy",me.localfontSize*1.2)
            .style("text-anchor","middle")
            .style("font-family","Neucha")
            .style("font-size",me.localfontSize+"pt")
            .text((d,i) => {
                let result = d;
                if (object_values){
                    result = d["text"]
                }
                if (cell_format.length > 0){
                    if (cell_format[i%rowlen] == "sols"){
                        let a = parseInt(d);
                        let b = (d-parseInt(d))*100;
                        result = ""
                        if (a>0)
                            result += ""+parseInt(a)+"s";
                        if (b>0)
                            result += " "+parseInt(b)+"d";

                    }
                    if (cell_format[i%rowlen] == "enc"){
                        if (d==0)
                            result = "-";
                    }
                }
                return result;
            })
//             .attr("opacity",0.25)
        ;
        table.append('text')
            .attr("x", (d,i) => {
                let result = me.paperX(rowlen)
                if (object_values){
                    result += me.localstep * 3.5
                }
                return result
            })
            .attr("y", (d,i) => me.paperY(-1.5))
            .style("text-anchor","middle")
            .style("font-family","Are You Serious")
            .style("font-size",me.localfontSize*3+"pt")
            .style("fill","#101010")
            .style("stroke","#606060")
            .style("stroke-width","0.25pt")
            .text(title)
        ;
        return table;
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


    drawAll(){
        let me = this;
        console.log(me.code)
        if (me.code == "SCREEN1"){
            me.supertitle = "Ecran n°1"
            me.drawBack();
            me.drawTable(me.config.data["STRESS_TABLE"],{"even_odd":true});
            me.drawTable(me.config.data["QUALITY_TABLE"],{"x":17, "y":0, "row_header_width": 3,"even_odd":true});
            me.drawTable(me.config.data["SOAK_TABLE"],{"x":34, "y":0});
            me.drawTable(me.config.data["PDOM_TABLE"],{"x":48, "y":0});
            me.drawTable(me.config.data["SUS_TABLE"],{"x":48, "y":15});
            me.drawTable(me.config.data["SCON_TABLE"],{"x":53, "y":0});
            me.drawTable(me.config.data["SECONDARIES_TABLE"],{"x":48, "y":25});
            me.drawTable(me.config.data["MISC_TABLE"],{"x":48, "y":35});
        }else if (me.code == "SCREEN4"){
            me.supertitle = "Ecran n°4"
            me.drawBack();

        }else if (me.code == "SCREEN2"){
            me.supertitle = "Ecran n°2"
            me.drawBack();
            me.drawTable(me.config.data["COMP_GENERIC_TABLE"],{"even_odd":true, "x":8, "y":0});
            me.drawTable(me.config.data["COMP_WEAPONS_TABLE"],{"even_odd":true, "x":0, "y":0});
            me.drawTable(me.config.data["COMP_PECULIAR_TABLE"],{"even_odd":true, "x":8, "y":16});
            me.drawTable(me.config.data["COMP_SPECIALIZED_TABLE"],{"even_odd":true, "x":16, "y":0});
            me.drawTable(me.config.data["COMP_KNOWLEDGE_TABLE"],{"even_odd":true, "x":16, "y":13});
            me.drawTable(me.config.data["COMP_DRACONIC_TABLE"],{"even_odd":true, "x":16, "y":25});




        }else if (me.code == "SCREEN3"){
            me.supertitle = "Ecran n°3"
            me.drawBack();
            me.drawTable(me.config.data["GEAR_TABLE_BAG"],{"x":-1, "y":0});
            me.drawTable(me.config.data["GEAR_TABLE_LAI"],{"x":-1, "y":22});
            me.drawTable(me.config.data["GEAR_TABLE_JUT"],{"x":-1, "y":42});
            me.drawTable(me.config.data["GEAR_TABLE_VEL"],{"x":-1, "y":55});

            me.drawTable(me.config.data["GEAR_TABLE_ECR"],{"x":10, "y":0});
            me.drawTable(me.config.data["GEAR_TABLE_FEU"],{"x":10, "y":14});
            me.drawTable(me.config.data["GEAR_TABLE_CUI"],{"x":10, "y":28});
            me.drawTable(me.config.data["GEAR_TABLE_OUT"],{"x":10, "y":51});

            me.drawTable(me.config.data["GEAR_TABLE_HBD"],{"x":21, "y":0});
            me.drawTable(me.config.data["GEAR_TABLE_SOI"],{"x":21, "y":12});
            me.drawTable(me.config.data["GEAR_TABLE_JOU"],{"x":21, "y":24});
            me.drawTable(me.config.data["GEAR_TABLE_LOC"],{"x":21, "y":42});

            me.drawTable(me.config.data["GEAR_TABLE_SUS"],{"x":32, "y":0});
            me.drawTable(me.config.data["GEAR_TABLE_HBS"],{"x":32, "y":12});
            me.drawTable(me.config.data["GEAR_TABLE_RED"],{"x":32, "y":26});
            me.drawTable(me.config.data["GEAR_TABLE_SEL"],{"x":32, "y":42});

            me.drawTable(me.config.data["GEAR_TABLE_MEL"],{"x":43, "y":0});
            me.drawTable(me.config.data["GEAR_TABLE_TIR"],{"x":43, "y":30});
            me.drawTable(me.config.data["GEAR_TABLE_LAN"],{"x":43, "y":37});
            me.drawTable(me.config.data["GEAR_TABLE_AMU"],{"x":43, "y":48});


        }else{
            me.drawBack();
            //if (me.co.tables.length > 0){
                let data = me.config.data[me.code];
                me.drawTable(data,{});
            //}
        }
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
        super.register();
        let me = this;
        me.co.axiomaticPerformers.push(me);
    }

    perform(code){
        super.perform();
        let me = this;
        me.init();
        console.log(me.config.data)
        me.code = code;
        me.drawAll();
        me.zoomActivate();
    }
}