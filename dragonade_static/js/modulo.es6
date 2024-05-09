class Modulo {
    constructor(co, config) {
        this.filename = 'test.svg'
        this.co = co;
        this.config = config;
        this.name = "Modulo";

    }


    drawPrint(){
        let me = this;
        let offsetx = 0.5;
        let offsety = 0.5;
        let click_1 = (e,d) => {
            me.saveSVG();
        }
        let click_2 = (e,d) => {
            me.createPDF();
        }
        let buttons = [
            {"id":"btn1","label": "Save as SVG","x":offsetx,"y":offsety,"click_action":click_1},
            {"id":"btn1","label": "Create PDF","x":offsetx,"y":offsety+1,"click_action":click_2}
        ]
        me.all_buttons = me.vis.append("g")
            .attr("class","do_not_print")
            .attr("id","all_buttons")
            .attr("transform",`translate(${me.ox*me.step},${me.oy*me.step})`)
        _.forEach(buttons,(v,k) => {
            let btn = me.all_buttons.append("g")
                .on("click", v.click_action);
            btn.append("rect")
                .attr("id","print_artefact")
                .attr("class","do_not_print")
                .attr("x",(v.x)*me.step)
                .attr("y",(v.y)*me.step)
                .attr("ry","3pt")
                .attr("rx","3pt")
                .attr("width",me.step*1.5 )
                .attr("height",me.step*0.8 )
                .attr('opacity',1)
                .style('stroke-width','2pt')
                .style('stroke','#606060')
                .style('fill','#C0F0C0')
            btn.append("text")
                .attr("id","print_artefact")
                .attr("class","do_not_print")
                .attr("x",(v.x+0.75)*me.step)
                .attr("y",(v.y)*me.step)
                .attr("dy",me.step/2)
                .attr('opacity',1)
                .style('stroke-width','0.25pt')
                .style('stroke','#606060')
                .style('fill','#101010')
                .style("text-anchor","middle")
                .style("font-size",me.fontSize+"pt")
                .style("font-family","Wellfleet")
                .text(v.label)
            ;
        });
    }

    zoomActivate() {
        let me = this;
        me.zoom = d3.zoom()
            .scaleExtent([0.5, 2])
            .on('zoom', function (event) {
                me.svg.attr('transform', event.transform)
            });
        me.vis.call(me.zoom);
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


    resizeEvent(){
        let me = this;
        console.log("ResizeEvent for "+me.name)
        let width = $(me.parent).width;
        let height = $(me.parent).height;
        //let boundingBox = document.querySelector("#svg_area").getBoundingClientRect();
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));

        me.vis
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h);
        ;
        me.svg.attr("transform", "translate("+me.w/2 +","+ me.h / 2+")")
    }

    drawCross(x,y){
        let me = this;
        let offset = 3;
        let cross = me.back.append('g')
            .attr('class', 'do_not_print')
        cross.append('line')
            .attr('x1', x)
            .attr('x2', x)
            .attr('y1', y-offset)
            .attr('y2', y+offset)
            .style('fill', 'transparent')
            .style('stroke', '#A02020')
            .style('stroke-width', '2pt')
        ;
        cross.append('line')
            .attr('x1',x-offset)
            .attr('x2', x+offset)
            .attr('y1', y )
            .attr('y2', y )
            .style('fill', '#A02020')
            .style('stroke', '#A02020')
            .style('stroke-width', '2pt')
        ;
        cross.append('text')
            .attr("x", x+offset*5)
            .attr("y", y+offset*5)
            .style("text-anchor","middle")
            .style("font-family","Wellfleet")
            .style("font-size","6pt")
            .style("fill","#A02020")
            .style("stroke","#202020")
            .style("stroke-width","0.25pt")
            .text(x+"/"+y)
        ;

    }

    action(type,str){
        let me = this;
        console.log(`${me.name} Nothing to do with action on [${x}] for this module! Please override action(str) in child module.`);
    }


    init() {
        let me = this;
//         console.log(me.name+" Init");
        me.debug = false;
        me.step = 50;
        me.basefont = "Wellfleet";
        me.fontSize = me.step / 8;
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
//         console.log(me.name+" Registered");
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
        let base_svg = d3.select(me.parent+" svg").html();
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
        let fname = me.filename;
        let nuke = document.createElement("a");
        nuke.href = 'data:application/octet-stream;base64,' + btoa(me.formatXml(exportable_svg));
        nuke.setAttribute("download", fname);
        nuke.click();
        me.svg.selectAll('.do_not_print').attr('opacity', 1);
    }

    createPDF() {
        let me = this;
        me.svg.selectAll('.do_not_print').attr('opacity', 0);
        let base_svg = d3.select("#print_area").html();

        let flist = '<style>';
//         console.log(me.config['fontset']);
        for (let f of me.config['fontset']) {

            flist += '@import url("https://fonts.googleapis.com/css2?family=' + f + '");';
        }
        flist += '</style>';
        let exportable_svg = '<?xml version="1.0" encoding="UTF-8" ?> \
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> \
<svg class="dragonade_paper" \
xmlns="http://www.w3.org/2000/svg" version="1.1" \
xmlns:xlink="http://www.w3.org/1999/xlink" width="' + me.width + '" height="' + me.height + '"> \
' + flist + base_svg + '</svg>';


//         lpage = "_" + (me.page + 1);

        let svg_name = me.fileprefix+"__" + me.filename + ".svg"
        let pdf_name = me.fileprefix+"__" + me.filename + ".pdf"
        let sheet_data = {
            'pdf_name': pdf_name,
            'svg_name': svg_name,
            'svg': exportable_svg
        }
        me.svg.selectAll('.do_not_print').attr('opacity', 1);
        $.ajax({
            url: 'ajax/svg2pdf/' + me.filename + '/',
            type: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: sheet_data,
            dataType: 'json',
            success: function (answer) {
                console.warn("PDF generated for [" + me.filename + "]...")
            },
            error: function (answer) {
                console.error('Error generating the PDF...');
                console.error(answer);
            }
        });
    }

    drawLongTextBlock(tgt,x,y,label,value,id){
        let me = this;
        let label_attrs = {
            "width":me.step*2,
            "height":me.step*0.5,
            "rx":me.step*0.1,
            "ry":me.step*0.1
            }
        let value_attrs = {
            "width":me.step*9.25,
            "height":me.step*0.75,
            "rx":me.step*0.1,
            "ry":me.step*0.1
        }
//         console.log("(**) ",value)
        me.drawBlock(tgt,x,y,label_attrs,value_attrs, label,value,id)
    }

    drawSmallNumericBlock(tgt,x,y,label,value,id){
        let me = this;
        let label_attrs = {
            "width":me.step*2,
            "height":me.step*0.4,
            "rx":me.step*0.1,
            "ry":me.step*0.1
            }
        let value_attrs = {
            "width":me.step*0.8,
            "height":me.step*0.4,
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
            "stroke-width":"0.5pt"
        }
        let value_styles = {
            "fill":"#F0F0F0",
            "stroke":"#808080",
            "stroke-width":"1pt"
        }
        let label_text_styles = {
            "font-family":"Abel",
            "font-size":me.fontSize+"pt",
            "text-anchor":"middle",
            "fill":"#F0F0F0",
            "stroke":"#C0C0C0",
            "stroke-width":"0.5pt"
        }
        let value_text_styles = {
            "font-family":"Wellfleet",
            "font-size":me.fontSize+"pt",
            "text-anchor":"start",
            "fill":"#101010",
            "stroke":"#C0C0C0",
            "stroke-width":"0.25pt",
        }
        let grp = tgt.append('g')
            .attr("id",id+"_grp")
            .attr("transform","translate("+x*me.step+","+y*me.step+")")
        grp.append('rect')
            .attrs({"x":0, "y":me.step*(-0.4/2) })
            .attrs(label_attrs)
            .styles(label_styles)
        grp.append('rect')
            .attr("id",id+"_rect")
            .attrs({"x":me.step*(2.1), "y":me.step*(-0.4/2) })
            .attrs(value_attrs)
            .styles(value_styles)
        grp.append('text')
            .attrs({"x":1*me.step, "y":0, "dy":me.fontSize/3+"pt" })
            .styles(label_text_styles)
            .text(label)
        grp.append('text')
            .attr("class","longwrap")
            .attr("id",id)
            .attr("x",me.step*2.25)
            .attr("y",0)
            .styles(value_text_styles)
            .text(value)
        if (me.debug == true){
            grp.append('circle')
                .attrs({"cx":0, "cy":0, "r":me.fontSize/3+"pt" })
                .styles({"fill":"red","stroke":"darkred","stroke-width":0.5+"pt"})
        }
    }

    dragonadeSignature(ox,oy,id,txt){
        let me = this
        let now = new Date()
        me.signature = me.stregoneria.append("g")
        me.stregoneria.append("g")
            .attr("id","signature_spot_"+id)
        d3.select("#signature_spot_"+id).append("image")
            .attr("class","relinkable")
            .attr("xlink:href", "static/main/svg/2024/dragonade.svg" )
            .attr("width",2.3*me.step)
            .attr("height",.6*me.step)
            .attr("x",ox*me.step)
            .attr("y",oy*me.step)
        me.signature.append("text")
            .attrs({"x":(ox+2.5)*me.step,"y":(oy+.4)*me.step})
            .styles({"font-family":"Neucha","text-anchor":"start","font-size":"8pt"})
            .text(txt+" ["+now.toLocaleDateString()+" "+now.toLocaleTimeString()+"]")

    }


    wrap(tgt, width) {
        let item = d3.select(tgt),
            words = item.text().split(/\s+/).reverse();
        let word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.3, // ems
            dy = 0,
            ox = parseFloat(item.attr("x")),
            oy = parseFloat(item.attr("y")),
            tspan = item.text(null).append("tspan").attr("x", ox).attr("y", oy).attr("dy", dy + "em");
        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(' '));
          if ((tspan.node().getComputedTextLength() >= width)||(word == "§")) {
            line.pop();
            tspan.text(line.join(" "));
            if (word=="§"){
                line = []
            }else{
                line = [word];
            }
            lineNumber += 1;
            tspan = item.append("tspan")
                .attr("x", ox)
                .attr("y", lineNumber * lineHeight + "em")
                .attr("dy", 0)
                .text(word+" ");
          }
        }
        return lineNumber
    }



    superwrap(tgt, width) {
        let me = this
        let item = d3.select(tgt),
            words = item.text().split(/\s+/).reverse();
        let word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.3, // ems
            dy = 0,
            ox = parseFloat(item.attr("x")),
            oy = parseFloat(item.attr("y")),
            tspan = item.text(null).append("tspan").attr("x", ox).attr("y", oy).attr("dy", dy + "em");
        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(' '));
          if ((tspan.node().getComputedTextLength() >= width)||(word == "§")) {
            line.pop();
            tspan.text(line.join(" "));
            if (word=="§"){
                line = []
            }else{
                line = [word];
            }
            lineNumber += 1;
            tspan = item.append("tspan")
                .attr("x", ox)
                .attr("y", lineNumber * lineHeight + "em")
                .attr("dy", 0)
                .text(word+" ");
          }
        }
        let bb = d3.select(tgt).node().getBoundingClientRect()
        item.append("rect")
            .attrs({"x":0,"y":0,"width":bb.width,"height":bb.height})
            .styles({"fill":"#a020202f","stroke":"#a02020","stroke-width":"1pt"})
        console.log("Superwrap >>",bb)
        return lineNumber
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
            me.xunits = 20;
            me.yunits = 28;

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
    }

   register(){
        let me = this;
        me.co.axiomaticPerformers.push(me);
    }


    perform() {
        let me = this;
        console.log(me.name+" Perform");
    }
}