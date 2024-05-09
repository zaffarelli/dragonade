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
        let colorSet = d3.scaleSequential()
                        .domain([1,20])
                        .interpolator(d3.interpolateViridis);
        me.version = "0.7";
        me.supertitle = "";
        me.fileprefix = "doc"
//         me.step = 50;
      //  me.fontSize = 0.2*me.step + "pt";
        me.basefont = "Wellfleet";
        // Drawing Size
        me.height = me.step * 29.7
        me.width = me.step * 21.0
        me.ox = 0
        me.oy = 0
        // View Size
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));
        me.font_size = me.step / 4 ;
        me.light = [0.70,0.4,0,0,0,0,0,0.40,0.70,0.90,1,0.90];
        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h);
        me.svg = me.vis.append('g')
            .attr("id", me.code)
            .attr("width", me.width+"cm")
            .attr("height", me.height+"cm")
            .append("svg:g")
            .attr("id","print_area")
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

//     drawBack(){
//         let me = this;
//         me.back = me.svg.append('g')
//             .attr("class","circlebacks")
//             .append("g")
//            // .attr("transform","translate("+(-me.step*21/2)+","+(-me.step*29.7/2)+")")
//         ;
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
//
//
//         me.drawPrint();
//
//         if (me.debug == true) {
//             me.xunits = 20;
//             me.yunits = 28;
//
//             let verticals = me.back.append('g')
//                 .attr('class', 'verticals do_not_print')
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
//                 .style('stroke', '#101010')
//                 .style('stroke-dasharray', '3 7')
//                 .style('stroke-width', '0.25pt');
//             let horizontals = me.back.append('g')
//                 .attr('class', 'horizontals do_not_print')
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
//                 .style('stroke', '#101010')
//                 .style('stroke-dasharray', '3 5')
//                 .style('stroke-width', '0.25pt');
//
//         }
//         me.back.append('text')
//             .attr("x", me.step*0.5)
//             .attr("y", me.step*20)
//             .attr("dy", 2*me.step/3)
//             .style("text-anchor","start")
//             .style("font-family","Wellfleet")
//             //.style("font-family","Henny Penny")
//             .style("font-size",me.fontSize+"pt")
//             .style("fill","#101010")
//             .style("stroke","#808080")
//             .style("stroke-width","0.25pt")
//             .text(me.supertitle)
//         ;

//     }

//     paperX(x){
//         let me = this;
//         let val = me.localx + x
//         val = val * me.localstep;
//         return val;
//     }
//
//     paperY(y){
//         let me = this;
//         let val = me.localy + y;
//         val = val * me.localstepy;
//         return val;
//     }
//



    drawTable(src, options){
        let me = this;
//         console.log(src)
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
        me.localx = me.ox + 0;
        me.localy = me.oy + 0;

        let offsetx = 1;
        let offsety = 1;


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
            .attr("transform","translate("+(me.step*offsetx)+","+(me.step*offsety)+")")
        me.localstep = me.step/2;
        me.localstepy = me.step/2*cell_height;
        me.localfontSize = 0.2*me.localstep;
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
            .attr("dy",me.localfontSize*cell_height+"pt")
            //.attr("dy",me.localfontSize*1.75+"pt")
            .style("text-anchor","middle")
            .style("font-family",me.basefont)
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
                .attr("rx", me.localstep/6)
                .attr("ry", me.localstep/6)
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
                .attr("stroke","#C0C0C0")
                .attr("stroke-width","0.5pt")
                .style("fill","#F0F0F0")
            ;
            cbh.append('text')
                .attr("x", (d,i) => me.paperX((i%rowlen)*2+1))
                .attr("y", (d,i) => me.paperY(collen+1-0.5))
                .style("text-anchor","middle")
                .style("font-family",me.basefont)
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
                .attr("rx", me.localstep/6)
                .attr("ry", me.localstep/6)
                .attr("width",me.localstep*1.9)
                .attr("height",me.localstep*0.8)
                .attr("stroke","#C0C0C0")
                .attr("stroke-width","0.5pt")
                .style("fill","#F0F0F0")
            ;
            rbh.append('text')
                .attr("x", (d,i) => me.paperX((rowlen)*2+1))
                .attr("y", (d,i) => me.paperY(i+0.5))
                .style("text-anchor","middle")
                .style("font-family",me.basefont)
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
                .attr("y", (d,i) => me.paperY(0))
                .style("text-anchor","middle")
                .style("font-family",me.basefont)
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
                let color = "#f0f0f0";
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
            .attr("dy",me.localfontSize*1.25+"pt")
            .style("text-anchor","middle")
            .style("font-family",me.basefont)
            .style("font-size",(d,i) => {
                let answer = me.localfontSize+"pt";
                if ("smallrid" in options){
                    answer = me.localfontSize/2+"pt";
                }
                return answer;
            })
            .style("fill","#401040")
            .style("stroke","#802080")
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
            .attr("dy",me.localfontSize*1.25+"pt")
            .style("text-anchor","middle")
            .style("font-family",me.basefont)
            .style("font-size",me.fontSize+"pt")
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
            //.style("font-family","Are You Serious")
            //.style("font-family","Smythe")
            .style("font-family","Griffy")
            .style("font-size",me.localfontSize*2+"pt")
            .style("fill","#101010")
            .style("stroke","#606060")
            .style("stroke-width","0.25pt")
            .text(title)
        ;
        if (me.debug){
            me.drawCross(me.paperX(0),me.paperY(0))
        }
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


    drawRosters(src,options){
        let me = this;
        let rw = 9;
        let rh = 19;
        let x = 0;
        let y = 0;
        me.infos = {};
        me.ss_lists = {};
        me.weapons_lists = {};
        me.armors_lists = {};
        me.spells_lists = {};
        me.shortcuts_lists = {};
        let tb = src["data"];
        me.localx = me.ox;
        me.localy = me.oy;
        if ("x" in options) {
            x = options["x"];
            me.localx = me.ox + options["x"];
        }

        if ("y" in options){
            y = options["y"];
            me.localy = me.oy + options["y"];
        }

        let subtb = tb.slice(0,3);
        if ("start" in options){
            subtb = tb.slice(options["start"],options["start"]+3);
        }
        me.localstep = me.step;
        me.localstepy = me.localstep;
        me.localfontSize = "8"


        let rosters = me.back.append("g")
            .attr('class', 'screen_rosters')
            .selectAll("screen_roster")
            .data(subtb)
            ;

        let roster_in = rosters.enter()
            .append("g")
            .attr("class","screen_roster")
            .attr("rid", (d) => d.rid)
            .attr("id", (d,i) => {
                me.infos[d["rid"]] = {"type":d.type};
                me.ss_lists[d["rid"]] = d["skills_summary"];
                me.weapons_lists[d["rid"]] = d["features"]["weapons"];
                me.armors_lists[d["rid"]] = d["features"]["armors"];
                me.spells_lists[d["rid"]] = d["features"]["spells"];
                me.shortcuts_lists[d["rid"]] = d["features"]["shortcuts"];
                return "screen_roster_"+i
            });
        roster_in.append('rect')
            .attr('x', (d,i) => me.paperX(i*(rw+0.5)) )
            .attr('y', (d,i) => me.paperY(0))
            .attr('rx', "10pt")
            .attr('ry', "10pt")
            .attr("width",rw*me.localstep)
            .attr("height",rh*me.localstep)
            .style("fill","white")
            .style("stroke","#101010")
            .style("stroke-width","2pt")
            ;
        roster_in.append('text')
            .attr('x', (d,i) => me.paperX(i*(rw+0.5)+4.5) )
            .attr('y', (d,i) => me.paperY(0+0.5) )
            .style("font-family","Griffy")
            .style("text-anchor","middle")
            .style("font-size",me.localfontSize*2+"pt")
            .style("fill","#101010")
            .style("stroke","#303030")
            .style("stroke-width","0.25pt")
            .text((d,i)=>d["name"])
            ;

        me.append_value_to(roster_in,2,0.5,"player",{"rw":rw,"label":false})
        me.append_value_to(roster_in,0.5,0.5,"misc.ENTRANCE",{"rw":rw,"label":false, "ta":"start"})


        roster_in.append('circle')
            .attr('cx', (d,i) => me.paperX(i*(rw+0.5)+0.5) )
            .attr('cy', (d,i) => me.paperY(0) )
            .attr("r",me.step/8)
            .style("fill",(d,i) => d["color"])
            .style("stroke","#101010")
            .style("stroke-width","1pt")
            ;

        roster_in.append('circle')
            .attr('cx', (d,i) => me.paperX(i*(rw+0.5)+(rw-0.5)) )
            .attr('cy', (d,i) => me.paperY(0) )
            .attr("r",me.step/8)
            .style("fill","white")
            .style("stroke","#101010")
            .style("stroke-width","1pt")
            ;


        let xo = 0.25;
        let yo = 0;
        let framed = {"width":"1pt","color":"#104080"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"AGI",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.AGI",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"CON",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.CON",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8
        me.append_value_to(roster_in,xo+0.5,yo+1,"FOR",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.FOR",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"TAI",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.TAI",{"rw":rw,"label":false})


        xo = 2.25;
        yo = 0;
        framed = {"width":"1pt","color":"#108040"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"EMP",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.EMP",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"ODG",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.ODG",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"OUI",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.OUI",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"VUE",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.VUE",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 1.6;
        framed = {"width":"1pt","color":"#804010"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"APP",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.APP",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"DEX",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.DEX",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"INT",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.INT",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"VOL",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.VOL",{"rw":rw,"label":false})

        xo = 2.25;
        yo = 1.6;
        me.append_value_to(roster_in,xo+0.5,yo+1,"DER",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.DER",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"LAN",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.LAN",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8
        me.append_value_to(roster_in,xo+0.5,yo+1,"MEL",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.MEL",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"TIR",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.TIR",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 3.2;
        me.append_value_to(roster_in,xo+0.5,yo+1,"FABLE",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.FAB",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"FAT",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.FAT",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"ENC",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.ENC",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"+PROT",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.PROT",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 4.0;
        me.append_value_to(roster_in,xo+0.5,yo+1,"SONGE",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.SON",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"SCO",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.SCO",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"SUS",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.SUS",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"+DOM",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.DOM",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 4.8;
        framed = {"width":"3pt","color":"#404040"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"REVE",{"rw":rw,"label":true, framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.REV",{"rw":rw,"label":false})
        xo += 1;
        me.append_value_to(roster_in,xo+0.5,yo+1,"VIE",{"rw":rw,"label":true, framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.VIE",{"rw":rw,"label":false})


        xo = 5;
        yo = 0;
        framed = {"width":"2pt","color":"#804080"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"IPG",{"rw":rw,"label":true,  framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.indice",{"rw":rw,"label":false})

        xo = 6.25;
//         me.append_value_to(roster_in,xo+0.5,yo+1,"IA",{"rw":rw,"label":true})
//         me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.indice_a",{"rw":rw,"label":false})

        xo = 7.5;
//         me.append_value_to(roster_in,xo+0.5,yo+1,"IS",{"rw":rw,"label":true, "ta":"middle"})
//         me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.indice_s",{"rw":rw,"label":false})


        xo = 5;
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"SEXE",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.GENDER",{"rw":rw,"label":false})

        xo = 6.25;
        me.append_value_to(roster_in,xo+0.5,yo+1,"MAIN",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.LEFTY",{"rw":rw,"label":false})

        xo = 7.5;
        me.append_value_to(roster_in,xo+0.5,yo+1,"Âge",{"rw":rw,"label":true, "ta":"middle"})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.AGE",{"rw":rw,"label":false})


        xo = 5
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"Taille (cm)",{"rw":rw,"label":true, "ta":"middle"})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.HEIGHT",{"rw":rw,"label":false})

        xo = 6.25;
        me.append_value_to(roster_in,xo+0.5,yo+1,"Poids (kg)",{"rw":rw,"label":true, "ta":"middle"})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.WEIGHT",{"rw":rw,"label":false})

        xo = 7.5;

        if (me.infos[roster_in.attr("rid")].type=="traveller"){
            me.append_value_to(roster_in,xo+0.5,yo+1,"Destinée",{"rw":rw,"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+0.5,yo+1.25,"destiny",{"rw":rw,"label":false})
        }else{
            me.append_value_to(roster_in,xo+0.5,yo+1,"Priorité",{"rw":rw,"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+0.5,yo+1.25,"priority",{"rw":rw,"label":false})
        }




        roster_in.append("g")
            .attr("class","skills_summary")
            .attr("id",(d,i) => "ss_for_"+d["rid"])
            ;
        me.append_list_to(me.ss_lists,{"rw":rw,"title":"COMPETENCES","target":"#ss_for_"})


        roster_in.append("g")
            .attr("class","weapons_summary")
            .attr("id",(d,i) => "weapons_for_"+d["rid"])
            ;
        me.append_wlist_to(me.weapons_lists,{"rw":rw,"title":"ARMES","target":"#weapons_for_"})

        roster_in.append("g")
            .attr("class","armors_summary")
            .attr("id",(d,i) => "armors_for_"+d["rid"])
            ;
        me.append_alist_to(me.armors_lists,{"rw":rw,"title":"ARMURES","target":"#armors_for_"})


        roster_in.append("g")
            .attr("class","spells_summary")
            .attr("id",(d,i) => "spells_for_"+d["rid"])
            ;
        me.append_slist_to(me.spells_lists,{"rw":rw,"title":"ARTS DRACONIQUES","target":"#spells_for_"})

        roster_in.append("g")
            .attr("class","shortcuts")
            .attr("id",(d,i) => "shortcut_"+d["rid"])
            ;
        me.append_sclist_to(me.shortcuts_lists,{"rw":rw,"title":"JETS","target":"#shortcut_"})



        let roster_out = rosters.exit().remove();
    }


    drawPortraitRosters(src,options){
        let me = this;
        let rw = 19;
        let rh = 14.5;
        let x = 1;
        let y = 1;
        me.infos = {};
        me.ss_lists = {};
        me.weapons_lists = {};
        me.armors_lists = {};
        me.spells_lists = {};
        me.shortcuts_lists = {};
        let tb = src["data"];
        me.localx = me.ox;
        me.localy = me.oy;
//         if ("x" in options) {
//             x = options["x"];
//             me.localx = options["x"];
//         }

//         if ("y" in options){
//             y = options["y"];
//             me.localy = options["y"];
//         }

        let subtb = tb.slice(0,3);
        if ("start" in options){
            subtb = tb.slice(options["start"],options["start"]+3);
        }
        me.localstep = me.step;
        me.localstepy = me.localstep;
        me.localfontSize = "8"


        let rosters = me.back.append("g")
            .attr('class', 'screen_rosters')
            .selectAll("screen_roster")
            .data(subtb)
            ;

        let roster_in = rosters.enter()
            .append("g")
            .attr("transform", (d,i) => `translate(${x*me.step},${(y+i*rh)*me.step})`)
            .attr("class","screen_roster")
            .attr("rid", (d) => d.rid)
            .attr("id", (d,i) => {
                me.infos[d["rid"]] = {"type":d.type};
                me.ss_lists[d["rid"]] = d["skills_summary"];
                me.weapons_lists[d["rid"]] = d["features"]["weapons"];
                me.armors_lists[d["rid"]] = d["features"]["armors"];
                me.spells_lists[d["rid"]] = d["features"]["spells"];
                me.shortcuts_lists[d["rid"]] = d["features"]["shortcuts"];
                return "screen_roster_"+i
            });
        roster_in.append('rect')
            .attr('x', (d,i) => me.paperX(0))
            .attr('y', (d,i) => me.paperY(-0.5))
            .attr('rx', "5pt")
            .attr('ry', "5pt")
            .attr("width",rw*me.localstep)
            .attr("height",(rh-0.5)*me.localstep)
            .style("fill","#F0F0F07f")
            .style("stroke","#101010")
            .style("stroke-width","2pt")
            ;
        roster_in.append('text')
            .attr('x', (d,i) => me.paperX(0.35) )
            .attr('y', (d,i) => me.paperY(0.0) )
            .style("font-family","Griffy")
            .style("text-anchor","start")
            .style("font-size",me.localfontSize*2+"pt")
            .style("fill","#101010")
            .style("stroke","#303030")
            .style("stroke-width","0.25pt")
            .text((d,i)=> {
                let s = d.name
                if (d.features.AKA != ""){
                    s += " (aka "+d.features.AKA+")"
                }
                return s
            })
            ;

        me.append_value_to(roster_in,rw-0.5,0,"player",{"rw":rw,"label":false, "ta":"end"})
        me.append_value_to(roster_in,0.5,0.5,"misc.ENTRANCE",{"rw":rw,"label":false, "ta":"start"})


        roster_in.append('circle')
            .attr('cx', (d,i) => me.paperX(0 ))
            .attr('cy', (d,i) => me.paperY(0.5) )
            .attr("r",me.step/8)
            .style("fill",(d,i) => d["color"])
            .style("stroke","#101010")
            .style("stroke-width","1pt")
            ;

        let xo = 0.25;
        let yo = 0;
        let framed = {"width":"1pt","color":"#104080"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"AGI",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.AGI",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"CON",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.CON",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8
        me.append_value_to(roster_in,xo+0.5,yo+1,"FOR",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.FOR",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"TAI",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.TAI",{"rw":rw,"label":false})


        xo = 2.25;
        yo = 0;
        framed = {"width":"1pt","color":"#108040"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"EMP",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.EMP",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"ODG",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.ODG",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"OUI",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.OUI",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"VUE",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.VUE",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 1.6;
        framed = {"width":"1pt","color":"#804010"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"APP",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.APP",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"DEX",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.DEX",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"INT",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.INT",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"VOL",{"rw":rw,"label":true, "framed" : framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"attributes.VOL",{"rw":rw,"label":false})

        xo = 2.25;
        yo = 1.6;
        me.append_value_to(roster_in,xo+0.5,yo+1,"DER",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.DER",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"LAN",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.LAN",{"rw":rw,"label":false})
        xo -= 1
        yo += 0.8
        me.append_value_to(roster_in,xo+0.5,yo+1,"MEL",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.MEL",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"TIR",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"secondaries.TIR",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 3.2;
        me.append_value_to(roster_in,xo+0.5,yo+1,"FABLE",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.FAB",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"FAT",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.FAT",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"ENC",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.ENC",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"+PROT",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.PROT",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 4.0;
        me.append_value_to(roster_in,xo+0.5,yo+1,"SONGE",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.SON",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"SCO",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.SCO",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"SUS",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.SUS",{"rw":rw,"label":false})
        xo += 1
        me.append_value_to(roster_in,xo+0.5,yo+1,"+DOM",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.DOM",{"rw":rw,"label":false})

        xo = 0.25;
        yo = 4.8;
        framed = {"width":"3pt","color":"#404040"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"REVE",{"rw":rw,"label":true, framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.REV",{"rw":rw,"label":false})
        xo += 1;
        me.append_value_to(roster_in,xo+0.5,yo+1,"VIE",{"rw":rw,"label":true, framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.VIE",{"rw":rw,"label":false})

        xo = 0.0;
        yo += 1.0;
        me.append_fatigue_points_to(roster_in,xo+0.5,yo+1.25,"misc.FAT",{"rw":rw,"label":false})
        me.append_life_points_to(roster_in,xo+2.5+0.25,yo+1.25,"misc.VIE",{"rw":rw,"label":false})

        xo = 5;
        yo = 0;
        framed = {"width":"2pt","color":"#804080"}
        me.append_value_to(roster_in,xo+0.5,yo+1,"IPG",{"rw":rw,"label":true,  framed})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.indice",{"rw":rw,"label":false})

        xo = 6.25;
//         me.append_value_to(roster_in,xo+0.5,yo+1,"IA",{"rw":rw,"label":true})
//         me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.indice_a",{"rw":rw,"label":false})

        xo = 7.5;
//         me.append_value_to(roster_in,xo+0.5,yo+1,"IS",{"rw":rw,"label":true, "ta":"middle"})
//         me.append_value_to(roster_in,xo+0.5,yo+1.25,"misc.indice_s",{"rw":rw,"label":false})


        xo = 5;
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"SEXE",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.GENDER",{"rw":rw,"label":false})

        xo = 6.25;
        me.append_value_to(roster_in,xo+0.5,yo+1,"MAIN",{"rw":rw,"label":true})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.LEFTY",{"rw":rw,"label":false})

        xo = 7.5;
        me.append_value_to(roster_in,xo+0.5,yo+1,"Âge",{"rw":rw,"label":true, "ta":"middle"})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.AGE",{"rw":rw,"label":false})


        xo = 5
        yo += 0.8;
        me.append_value_to(roster_in,xo+0.5,yo+1,"Taille (cm)",{"rw":rw,"label":true, "ta":"middle"})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.HEIGHT",{"rw":rw,"label":false})

        xo = 6.25;
        me.append_value_to(roster_in,xo+0.5,yo+1,"Poids (kg)",{"rw":rw,"label":true, "ta":"middle"})
        me.append_value_to(roster_in,xo+0.5,yo+1.25,"features.WEIGHT",{"rw":rw,"label":false})

        xo = 7.5;

        if (me.infos[roster_in.attr("rid")].type=="traveller"){
            me.append_value_to(roster_in,xo+0.5,yo+1,"Destinée",{"rw":rw,"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+0.5,yo+1.25,"destiny",{"rw":rw,"label":false})
        }else{
            me.append_value_to(roster_in,xo+0.5,yo+1,"Priorité",{"rw":rw,"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+0.5,yo+1.25,"priority",{"rw":rw,"label":false})
        }




        roster_in.append("g")
            .attr("class","skills_summary")
            .attr("id",(d,i) => "ss_for_"+d["rid"])
            ;
        me.append_list_to(me.ss_lists,{"rw":rw,"title":"COMPETENCES","target":"#ss_for_"})


        roster_in.append("g")
            .attr("class","weapons_summary")
            .attr("id",(d,i) => "weapons_for_"+d["rid"])
            ;
        me.append_wlist_to(me.weapons_lists,{"rw":rw,"title":"ARMES","target":"#weapons_for_"})

        roster_in.append("g")
            .attr("class","armors_summary")
            .attr("id",(d,i) => "armors_for_"+d["rid"])
            ;
        me.append_alist_to(me.armors_lists,{"rw":rw,"title":"ARMURES","target":"#armors_for_"})


        roster_in.append("g")
            .attr("class","spells_summary")
            .attr("id",(d,i) => "spells_for_"+d["rid"])
            ;
        me.append_slist_to(me.spells_lists,{"rw":rw,"title":"ARTS DRACONIQUES","target":"#spells_for_"})

        roster_in.append("g")
            .attr("class","shortcuts")
            .attr("id",(d,i) => "shortcut_"+d["rid"])
            ;
        me.append_sclist_to(me.shortcuts_lists,{"rw":rw,"title":"JETS","target":"#shortcut_"})



        let roster_out = rosters.exit().remove();
    }



    append_value_to(tgt,x,y,str,options){
        let me = this;
        let ta = "middle"
        if ("ta" in options){
            ta = options["ta"]
        }
        let stk = "#808080"
        if ("bold" in options){
            stk = "#101010"
        }
        if ("framed" in options){
            tgt.append('rect')
                .attr('x', (d,i) => me.paperX(x-0.4) )
                .attr('y', (d,i) => me.paperY(y-0.25) )
                .attr("width",me.localstep*0.8)
                .attr("height",me.localstep*0.6)
                .style("fill","#F0F0F0")
                .style("stroke",options['framed']['color'])
                .style("stroke-width",options['framed']['width'])
            ;
        }
        tgt.append('text')
            .attr('x', (d,i) => me.paperX(x) )
            .attr('y', (d,i) => me.paperY(y) )
            .style("font-family","Wellfleet")
            .style("text-anchor",ta)
            .style("font-size",me.localfontSize+"pt")
            .style("fill","#101010")
            .style("stroke",stk)
            .style("stroke-width","0.25pt")
            .text((d,i)=>{

                let struct = d;
                let answer = d[str]
                if (("label" in options) && (options["label"] == true)){
                    answer = str
                }else{
                    let words = str.split(".");
                    if (words.length>1){
                        words.forEach((k) => {
                            //console.log(k)
                            if (k in struct){
                                struct = struct[k]
                            }
                        })
                        answer = struct
                    }
                }
                return answer
            })
        ;

    }

    append_fatigue_points_to(tgt,x,y,str,options){
        let me = this;
        let ta = "middle"
        if ("ta" in options){
            ta = options["ta"]
        }
        let stk = "#808080"
        if ("bold" in options){
            stk = "#101010"
        }

        let struct = {}
        let val = 0

        tgt.append('g')
            .attr("class", (d)=>{
                let struct = d;
                let answer = d[str]
                let words = str.split(".");
                if (words.length>1){
                    words.forEach((k) => {
                        if (k in struct){
                            struct = struct[k]
                        }
                    })
                    val = parseInt(struct)
                }
            })
       let ly = -0.25
       let lx = -0.25
       tgt.append('text')
            .attr('x', (d,i) => me.paperX(x+lx) )
            .attr('y', (d,i) => me.paperY(y+ly) )
            .style("fill","#303030")
            .style("stroke","#101010")
            .style("stroke-width","0.5pt")
            .style("font-family","Wellfleet")
            .style("text-anchor","start")
            .style("font-size",me.localfontSize+"pt")
            .text("Points de Fatigue")
        ly += 0.25

        console.log("Fatigue Val:",val)
        while(val>0){
            let amount = 2 + Math.ceil(val/2)
            lx = -0.25
            while (amount>0){
                tgt.append('circle')
                    .attr('cx', (d,i) => me.paperX(x+lx+0.1) )
                    .attr('cy', (d,i) => me.paperY(y+ly+0.1) )
                    .attr("r",me.step*0.1)
                    //.attr("height",me.step*0.2)
                    .style("fill","#F0F0F0")
                    .style("stroke","#101010")
                    .style("stroke-width","0.5pt")
                amount -= 1
                lx += 0.25
            }
            ly += 0.25
            val -= 1
        }
    }

    append_life_points_to(tgt,x,y,str,options){
        let me = this;
        let ta = "middle"
        if ("ta" in options){
            ta = options["ta"]
        }
        let stk = "#808080"
        if ("bold" in options){
            stk = "#101010"
        }

        let struct = {}
        let val = 0

        tgt.append('g')
            .attr("class", (d)=>{
                let struct = d;
                let answer = d[str]
                let words = str.split(".");
                if (words.length>1){
                    words.forEach((k) => {
                        if (k in struct){
                            struct = struct[k]
                        }
                    })
                    val = parseInt(struct)
                }
            })
       let ly = -0.25
       let lx = -0.25
       tgt.append('text')
            .attr('x', (d,i) => me.paperX(x+lx) )
            .attr('y', (d,i) => me.paperY(y+ly) )
            .style("fill","#303030")
            .style("stroke","#101010")
            .style("stroke-width","0.5pt")
            .style("font-family","Wellfleet")
            .style("text-anchor","start")
            .style("font-size",me.localfontSize+"pt")
            .text("Points de Vie")
        ly += 0.1

       console.log("Life Val:",val)
       let baseval = val
       val = 0
       while(val<baseval){
            console.log(baseval,val)
            ly = Math.floor(val / 5)*0.25
            lx = (val % 5)*0.25
            tgt.append('rect')
                .attr('x', (d,i) => me.paperX(x+lx-0.25) )
                .attr('y', (d,i) => me.paperY(y+ly) )
                .attr("width",me.step*0.2)
                .attr("height",me.step*0.2)
                .style("fill","#F0F0F0")
                .style("stroke","#101010")
                .style("stroke-width","0.5pt")
            val += 1
       }
    }


    append_list_to(list,options){
        // skills
        let me = this;
        let xoffset = 0
        _.forEach(list, (v,k) => {
            let roster_in = d3.select(options["target"]+k);
            let xo = me.ox + 9 ;
            let yo = me.oy + 1  ;
            me.append_value_to(roster_in,xo+0.25,yo-0.5,options["title"],{"rw":options['rw'],"label":true, "ta":"start", "bold":true})
            v.forEach((x,i) => {
                me.append_value_to(roster_in,xo+0.25,yo,x["text"]+" ("+x["category"]+")" ,{"rw":options['rw'],"label":true, "ta":"start"})
                me.append_value_to(roster_in,xo+2.95,yo,x["value"],{"rw":options['rw'],"label":true, "ta":"middle"})
                yo += 0.25;
                if (i%5==4){
                    yo += 0.10;
                }
                if (i%50==49){
                    yo -= 15*0.25+3*0.10
                    xo += 3.15;
                }
            });
            if (v.length == 0){
                me.append_value_to(roster_in,xo+0.25,yo,"-",{"rw":options['rw'],"label":true, "ta":"start"})
            }
            xoffset += 1;
        });
    }

    append_wlist_to(list,options){
        // Weapon List
        let me = this;
        let xoffset = 0
        _.forEach(list, (v,k) => {
            let roster_in = d3.select(options["target"]+k);
            //let xo = me.ox + xoffset * (options["rw"] + 0.5);
            let xo = me.ox + 0 ;
            let yo = me.oy + 10.5  ;
            me.append_value_to(roster_in,xo+0.25,yo,options["title"],{"rw":options['rw'],"label":true, "ta":"start", "bold":true})
            me.append_value_to(roster_in,xo+3.30,yo,"INI",{"rw":options['rw'],"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+3.80,yo,"VAL",{"rw":options['rw'],"label":true, "ta":"middle"})
            let previous_cat = "";
            v.forEach((x,i) => {
                if (previous_cat != x["category"]){
                    yo += 0.25;
                    previous_cat = x["category"]
                }
                me.append_value_to(roster_in,xo+0.25,yo,x["name"]+"("+x["dom_1"]+"/"+x["dom_2"]+")" ,{"rw":options['rw'],"label":true, "ta":"start", "bold":true})
                me.append_value_to(roster_in,xo+3.30,yo,x["init"],{"rw":options['rw'],"label":true, "ta":"middle"})
                me.append_value_to(roster_in,xo+3.80,yo,x["score"],{"rw":options['rw'],"label":true, "ta":"middle"})
                yo += 0.25;
                if (i%3==2){
                    yo += 0.10 ;
                }
            });
            if (v.length == 0){
                me.append_value_to(roster_in,xo+0.25,yo,"-",{"rw":options['rw'],"label":true, "ta":"start"})
            }
            xoffset += 1;
        });
    }

    append_alist_to(list,options){
        // Armor list
        let me = this;
        let xoffset = 0
        _.forEach(list, (v,k) => {
            let roster_in = d3.select(options["target"]+k);
            let xo = me.ox + 0 ;
            let yo = me.oy + 9.5  ;
            me.append_value_to(roster_in,xo+0.25,yo,options["title"],{"rw":options['rw'],"label":true, "ta":"start", "bold":true})
            me.append_value_to(roster_in,xo+3.30,yo,"MA",{"rw":options['rw'],"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+3.80,yo,"PROT",{"rw":options['rw'],"label":true, "ta":"middle"})
            yo += 0.25;
            v.forEach((x,i) => {
                me.append_value_to(roster_in,xo+0.25,yo,x["name"] ,{"rw":options['rw'],"label":true, "ta":"start"})
                me.append_value_to(roster_in,xo+3.30,yo,x["malus_armure"],{"rw":options['rw'],"label":true, "ta":"middle"})
                me.append_value_to(roster_in,xo+3.80,yo,x["prot"],{"rw":options['rw'],"label":true, "ta":"middle"})
                yo += 0.25;
            });
            if (v.length == 0){
                me.append_value_to(roster_in,xo+0.25,yo,"-",{"rw":options['rw'],"label":true, "ta":"start"})
            }
            xoffset += 1;
        });

    }

    append_slist_to(list,options){
        // Spells list
        let me = this;
        let xoffset = 0
        _.forEach(list, (v,k) => {
            let roster_in = d3.select(options["target"]+k);
            let xo = me.ox + 12.5;
            let yo = me.oy + 0.5  ;
            me.append_value_to(roster_in,xo+0.10,yo,options["title"],{"rw":options['rw'],"label":true, "ta":"start", "bold":true})
            me.append_value_to(roster_in,xo+3.60,yo,"PdR",{"rw":options['rw'],"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+4.10,yo,"DIFF",{"rw":options['rw'],"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+4.70,yo,"Roll",{"rw":options['rw'],"label":true, "ta":"middle"})
            me.append_value_to(roster_in,xo+5.20,yo,"Cat",{"rw":options['rw'],"label":true, "ta":"middle"})
            yo += 0.25;
            v.forEach((x,i) => {

                me.append_value_to(roster_in,xo+0.10,yo,x["name"] ,{"rw":options['rw'],"label":true, "ta":"start"})
                me.append_value_to(roster_in,xo+3.60,yo,x["dps"],{"rw":options['rw'],"label":true, "ta":"middle"})
                me.append_value_to(roster_in,xo+4.10,yo,x["diff"],{"rw":options['rw'],"label":true, "ta":"middle"})
                me.append_value_to(roster_in,xo+4.70,yo,x["roll"],{"rw":options['rw'],"label":true, "ta":"middle"})
                me.append_value_to(roster_in,xo+5.20,yo,x["category"][0],{"rw":options['rw'],"label":true, "ta":"middle"})
                yo += 0.25;
            });
            if (v.length == 0){
                me.append_value_to(roster_in,xo+0.25,yo,"-",{"rw":options['rw'],"label":true, "ta":"start"})
            }
            xoffset += 1;
        });
    }

    append_sclist_to(list,options){
        // Short Cuts
        let me = this;
        let xoffset = 0
        _.forEach(list, (v,k) => {
            let roster_in = d3.select(options["target"]+k);
            let xo = me.ox + 4.5 ;
            let yo = me.oy + 3.5  ;
            me.append_value_to(roster_in,xo+0.25,yo,options["title"],{"rw":options['rw'],"label":true, "ta":"start", "bold":true})
            me.append_value_to(roster_in,xo+3.75,yo,"Score",{"rw":options['rw'],"label":true, "ta":"middle"})

            yo += 0.25;
            v.forEach((x,i) => {
                me.append_value_to(roster_in,xo+0.25,yo,x["roll"] ,{"rw":options['rw'],"label":true, "ta":"start"})
                me.append_value_to(roster_in,xo+3.75,yo,x["val"],{"rw":options['rw'],"label":true, "ta":"middle"})
                yo += 0.25;
            });
            xoffset += 1;
        });
    }

    append_fatiguePoints(tgt, x,y){

    }

    drawAll(){
        let me = this;
        if (me.code == "SCREEN1"){
            me.supertitle = "Ecran n°1"
            me.drawBack();
            me.drawTable(me.config.data["STRESS_TABLE"],{"x":0.5, "y":0.5,"even_odd":true});
            me.drawTable(me.config.data["QUALITY_TABLE"],{"x":17, "y":0.5, "row_header_width": 3,"even_odd":true});
            me.drawTable(me.config.data["PDOM_TABLE"],{"x":37, "y":5});
            me.drawTable(me.config.data["SUS_TABLE"],{"x":37, "y":20});
            me.drawTable(me.config.data["SCON_TABLE"],{"x":37, "y":35});

            me.drawTable(me.config.data["COMP_WEAPONS_TABLE"],{"even_odd":true, "x":15, "y":13});
            me.drawTable(me.config.data["COMP_GENERIC_TABLE"],{"even_odd":true, "x":22, "y":13});
            me.drawTable(me.config.data["COMP_PECULIAR_TABLE"],{"even_odd":true, "x":22, "y":30});
            me.drawTable(me.config.data["COMP_SPECIALIZED_TABLE"],{"even_odd":true, "x":29, "y":13});
            me.drawTable(me.config.data["COMP_KNOWLEDGE_TABLE"],{"even_odd":true, "x":29, "y":26});
            me.drawTable(me.config.data["COMP_DRACONIC_TABLE"],{"even_odd":true, "x":29, "y":38});

            me.drawTable(me.config.data["SECONDARIES_TABLE"],{"x":2, "y":34});
            me.drawTable(me.config.data["MISC_TABLE"],{"x":2, "y":41});
        }else if (me.code == "SCREEN2"){
            me.supertitle = "Ecran n°2"
            me.drawBack();
            me.drawTable(me.config.data["GEAR_TABLE_BAG"],{"x":3, "y":1, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_LAI"],{"x":3, "y":23, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_JUT"],{"x":3, "y":43, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_VEL"],{"x":3, "y":56, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_ECR"],{"x":3, "y":71, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_FEU"],{"x":3, "y":86, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_TIR"],{"x":3, "y":101, "smallrid":true});

            me.drawTable(me.config.data["GEAR_TABLE_HBD"],{"x":15, "y":1, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_SOI"],{"x":15, "y":13, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_JOU"],{"x":15, "y":25, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_LOC"],{"x":15, "y":41, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_CUI"],{"x":15, "y":56, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_OUT"],{"x":15, "y":81, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_LAN"],{"x":15, "y":105, "smallrid":true});

            me.drawTable(me.config.data["GEAR_TABLE_SUS"],{"x":27, "y":1, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_HBS"],{"x":27, "y":13, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_RED"],{"x":27, "y":27, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_SEL"],{"x":27, "y":43, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_AMU"],{"x":27, "y":55, "smallrid":true});
            me.drawTable(me.config.data["GEAR_TABLE_MEL"],{"x":27, "y":67, "smallrid":true});
        }else if (me.code == "SCREEN3"){
            me.supertitle = "Ecran n°3"
            me.drawBack();
        }else if (me.code == "SCREEN4"){
            me.supertitle = "Ecran n°4"
            me.drawBack();
        }else if (me.code == "SCREEN5"){
            me.supertitle = "Ecran n°5"
            me.drawBack();
        }else if (me.code.startsWith("AUTOCHTONS")){
            me.supertitle = me.code
            me.drawBack();
            me.drawPortraitRosters(me.config.data[me.code],{"x":1, "y":1, "start":0});
        }else if (me.code.startsWith("TRAVELLERS")){
            me.supertitle = me.code
            me.drawBack();
            me.drawPortraitRosters(me.config.data[me.code],{"x":1, "y":1, "start":0});
        }else{
            me.drawBack();
            let data = me.config.data[me.code];
            me.drawTable(data,{});
        }
    }

//     zoomActivate() {
//         let me = this;
//         me.zoom = d3.zoom()
//             .scaleExtent([0.25, 4])
//             .on('zoom', function (event) {
//                 me.svg.attr('transform', event.transform)
//             });
//         me.vis.call(me.zoom);
//     }

//    register(){
//         super.register();
//         let me = this;
//         me.co.axiomaticPerformers.push(me);
//     }

    perform(code){
        super.perform();
        let me = this;
        me.init();
        console.log(me.config.data)
        me.code = code;
        me.filename = me.code
        me.drawAll();
        me.zoomActivate();
    }
}