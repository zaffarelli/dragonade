class Appartus extends Modulo {
    constructor(co, config) {
        super(co, config);
        this.name = "Appartus";
        this.parent = "#svg_area";
        this.fetched = false
    }

    init() {
        super.init()
        let me = this
        me.version = "1.0.0"
        me.supertitle = ""
        me.fontSize = 10
        // Drawing Size
        me.height = me.step * 21.0
        me.width = me.step * 29.7 / 2
        me.ox = 0
        me.oy = 0
        // View Size
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));
        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h)
        me.svg = me.vis.append('g')
            .attr("id", me.code)
            .attr("width", me.width)
            .attr("height", me.height)
            .append("svg:g")
            .attr("id", "print_area")
            .attr("transform", "translate(0,0)")
    }


    drawAppartus() {
        let me = this;
        let a = me.datum.payload
        let ox = 0.5, oy = 1.5
        // Statistics
        me.artefatto = me.back.append("g")
            .attr("class", "artefatto")
            .attr("id", "artefatto_" + a.rid)
            .attr("transform", "translate(" + ox * me.step + "," + oy * me.step + ")")
        me.artefatto.append('rect')
            .attr("class", "rect_top")
            .attrs({
                "x": 0 * me.step,
                "y": me.step * 0,
                "rx": me.step * 0.1,
                "ry": me.step * 0.1,
                "width": me.step * (29.7 / 2 - 1.75),
                "height": me.step * 2.5
            })
            .style("fill", "#ffffff")
            .style("stroke", "black")
            .style("stroke-width", "1pt")
        me.artefatto.append('rect')
            .attr("class", "rect_bottom")
            .attr("id", "rectbot")
            .attrs({"x": 0, "y": me.step * 2.75, "rx": me.step * 0.1, "ry": me.step * 0.1, "width": (me.step * (29.7 / 2 - 1.75)), "height": me.step * 15.75})
            .style("fill", "#ffffff")
            .style("stroke", "black")
            .style("stroke-width", "1pt")
        me.artefatto.append('text')
            .attrs({"x": me.step * 0.25, "y": (-0.25) * me.step})
            .styles({"font-family": me.titleFont, "font-size": me.fontSize * 4 + "pt", "text-anchor": "start"})
            .text(a.name)
        // me.artefatto.append('text')
        //     .attrs({"x": me.step * 13.75, "y": -0.25 * me.step})
        //     .styles({"font-family": "Wellfleet", "font-size": me.fontSize * 4 + "pt", "text-anchor": "end"})
        //     .text(a.power)
        let basex = 0.5
        let basey = 15.5
        me.artefatto.append("circle")
                .attrs({"cx":(basex+12.5)*me.step,"cy":(basey-15.50)*me.step,"r":0.5*me.step})
                .styles({"fill":"white","stroke-width":"2pt","stroke-dasharray":"","stroke":"black"})
        me.artefatto.append('text')
            .attrs({"x":(basex+12.5)*me.step,"y":(basey-15.35)*me.step})
            .styles({"font-family":me.altFont, "font-size":me.fontSize*2+"pt", "text-anchor":"middle"})
            .text(a.power)
        let lh = 0.5 * 2 / 3 * me.step
        let delx = 4
        let metrics = [
            {x: (delx * 0) + 0.25, y: 0.5, label: "Maîtrise", value: a.mastery, "id": "met1"},
            {x: (delx * 0) + 0.25, y: 1, label: "Inertie", value: a.inertia, "id": "met2"},
            {x: (delx * 0) + 0.25, y: 1.5, label: "Activation", value: a.pdr, "id": "met3"},
            {x: (delx * 0) + 0.25, y: 2.0, label: "Période", value: a.period_str, "id": "met4"},
            {x: (delx * 1) + 0.25, y: 0.5, label: "Gemmes", value: a.gems_str, "id": "met5"},
            {x: (delx * 1) + 0.25, y: 1, label: "Ecailles", value: "", "id": "met6"},
            {x: (delx * 1) + 0.25, y: 1.5, label: "Categorie", value: a.category_str, "id": "met7"},
            {x: (delx * 1) + 0.25, y: 2, label: "", value: "", "id": "met8"},
            {x: (delx * 2) + 0.25, y: 0.5, label: "", value: "", "id": "met9"},
            {x: (delx * 2) + 0.25, y: 1, label: "Modif. Init", value: me.signed(a.mod_ini), "id": "met10"},
            {x: (delx * 2) + 0.25, y: 1.5, label: "Modif. Man.", value: me.signed(a.mod_man), "id": "met11"},
            {x: (delx * 2) + 0.25, y: 2.0, label: "Modif DOMA", value: me.signed(a.mod_dmg), "id": "met12"}
        ]
        _.forEach(metrics, (e) => {
            me.drawSmallNumericBlock(me.artefatto, e.x, e.y, e.label, e.value)
        })
        let stack_y = 13.5
        let text_metrics = [
            {x: 0.25, y: stack_y, label: "Apparence", value: a.glance, id: "att1"},
            {x: 0.25, y: stack_y, label: "Possesseur", value: a.owner, id: "att2"},
            {x: 0.25, y: stack_y, label: "Matériaux", value: a.materials, id: "att3"},
            {x: 0.25, y: stack_y, label: "Créateur", value: a.creator, id: "att4"},
            {x: 0.25, y: stack_y, label: "Description", value: a.description, id: "att5"},
            {x: 0.25, y: stack_y, label: "Règles", value: a.rules, id: "att6"},
            {x: 0.25, y: stack_y, label: "Notes", value: a.notes, id: "att7"}
        ]

        _.forEach(text_metrics, (e) => {
            me.drawLongTextBlock(me.artefatto, e.x, e.y, e.label, e.value, e.id, e.edit_field)
        })

        let wrap_width = 9.5 * me.step
        let cnts = [0]
        let blocks = [1,2,3,4,5,6,7]
        let bulks = [0]
        let bo = 0
        _.forEach(blocks,(v,k)=> {
            let lc = me.superwrap(`#att${v}`, wrap_width) + 1
            cnts.push(lc)
            bo += lc+1
            bulks.push(bo)
            d3.select(`#att${v}_rect`).attr("height", cnts[k] * lh)
            d3.select(`#att${v}_grp`)
                .attr("transform", "translate(" + (0.25 * me.step) + "," + (0.5 * me.step * stack_y+(bulks[k]*lh)) + ")")
        })
        // Emplacements des écailles
        let y_pos = 4
        _.forEach([1, 2, 3, 4, 5, 6, 7], (e) => {
            let offset_x = (e * 1.75 - 0.5) * me.step
            me.artefatto.append("circle")
                .attrs({"cx": offset_x, "cy": (y_pos - 0.05) * me.step, "r": 0.6 * me.step})
                .styles({"fill": "#F0F0F0", "stroke-width": "5pt", "stroke": "#808080"})
            me.artefatto.append("circle")
                .attrs({"cx": offset_x, "cy": (y_pos - 0.8) * me.step, "r": 0.2 * me.step})
                .styles({"fill": "#808080", "stroke": "none"})
            me.artefatto.append('text')
                .attrs({"x": offset_x, "y": me.step * (y_pos - 0.8), "dy": "3pt"})
                .styles({
                    "fill": "#101010",
                    "stroke": "#404040",
                    "stroke-width": "0.5pt",
                    "font-family": "Wellfleet",
                    "font-size": "8pt",
                    "text-anchor": "middle"
                })
                .text(e)
        })
        // Ecailles
        let ecailles = a.scales.split(" ")
        _.forEach(ecailles, (v, k) => {
            let offset_x = ((k + 1) * 1.75 - 0.5) * me.step
            me.drawScale(me.artefatto, offset_x, me.step * y_pos, v)
        })

        // Emplacements des Gemmes
        y_pos = 5.75
        _.forEach(a.all_gems, (e,k) => {
            let offset_x = ((k+1) * 1.75 - 0.5) * me.step
            me.artefatto.append("circle")
                .attrs({"cx": offset_x, "cy": (y_pos - 0.05) * me.step, "r": 0.6 * me.step})
                .styles({"fill": "#F0F0F0", "stroke-width": "5pt", "stroke": "#808080"})
            me.artefatto.append("circle")
                .attrs({"cx": offset_x, "cy": (y_pos - 0.8) * me.step, "r": 0.2 * me.step})
                .styles({"fill": "#808080", "stroke": "none"})
            me.artefatto.append('text')
                .attrs({"x": offset_x, "y": me.step * (y_pos - 0.8), "dy": "3pt"})
                .styles({
                    "fill": "#101010",
                    "stroke": "#404040",
                    "stroke-width": "0.5pt",
                    "font-family": "Wellfleet",
                    "font-size": "8pt",
                    "text-anchor": "middle"
                })
                .text(e.attachment)
        })


        me.dragonadeSignature(.75, 20, a.rid, "Fiche d'Artefact: " + a.name)
    }

    drawScale(tgt, x, y, scale) {
        let me = this
        let sc = tgt.append('g')
            .attr('class', "scale")
        let icon = sc.append('g')
            .attr('class', 'icon')
            .attr('transform', 'translate(' + (x) + ',' + (y) + ')')
        icon.append("image")
            .attr('transform', 'translate(' + (-33) + ',' + (-36) + ')')
            .attr("xlink:href", "static/main/svg/2026/" + scale + ".svg")
            .style('width', (me.step) + "pt")
        // icon.append("circle")
        //     .attr("r","1pt")
        //     .styles({"stroke-width":"1pt","stroke":"none","fill":"red"})
    }

    perform(code) {
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

    postFetch() {
        super.postFetch()
        let me = this
        me.fetched = true
        me.drawBack()
        me.drawAppartus()
        me.zoomActivate()
    }

    goBack() {
        super.goBack()
        $("#svg_area").remove()
    }

    handle(code) {
        super.handle()
        let me = this
        me.code = code
        me.fileprefix = "artefatto"
        me.filename = me.code
        $("<div id='svg_area'></div>").insertBefore('.zlist_container')
        me.init()
        me.fetch("artefatto", code)

    }


}