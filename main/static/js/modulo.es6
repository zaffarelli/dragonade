class Modulo {
    constructor(co, config) {
        this.filename = 'test.svg'
        this.co = co;
        this.config = config;
        this.name = "Modulo";
    }


    drawPrint(){
        let me = this;
        me.back.append("rect")
            .attr("id","print_artefact")
            .attr("class","do_not_print")
            .attr("x",-me.ox*me.step)
            .attr("y",me.oy*me.step)
            .attr("ry","5pt")
            .attr("rx","5pt")
            .attr("width",me.step/2 )
            .attr("height",me.step/2 )
            .attr('opacity',1)
            .style('stroke-width','2pt')
            .style('stroke','#603060')
            .style('fill','#F0F0F0')
            .on("click", (e,d) => {
                me.filename = "file.svg";
                me.saveSVG();
            });
        ;
        me.back.append("text")
            .attr("id","print_artefact")
            .attr("class","do_not_print")
            .attr("x",-me.ox*me.step+0.25*me.step)
            .attr("y",me.oy*me.step)
            .attr("dy",me.step/3)
            .attr('opacity',1)
            .style('stroke-width','0.25pt')
            .style('stroke','#606060')
            .style('fill','#101010')
            .style("text-anchor","middle")
            .style("font-size","8pt")
            .style("font-family","Neucha")
            .text("Save")
        ;
    }




    init() {
        let me = this;
        console.log(me.name+" Init");
        me.debug = true;
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
        console.log(me.name+" Registered");
    }

    resizeEvent(){
        let me = this;
        console.log(me.name+" received resizeEvent ");
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

    perform() {
        let me = this;
        console.log(me.name+" Perform");
    }
}