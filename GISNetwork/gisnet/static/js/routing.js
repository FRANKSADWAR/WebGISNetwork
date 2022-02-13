(function(){
    var geoserverUrl ="http://localhost:8080/geoserver/routing";
    var source,target,selectedPoint;

    function pathStyle(feature){
        return {
            weight:2,
            opacity:0.9,
            color:'blue',
            dashArray :'3',
        };
    }
    
    var pathLayer = L.geoJSON(null,{
        style:pathStyle(pathLayer),
    });
    
    // INITIALIZE THE MAP
    var map = L.map('storemaps').setView([-1.313261,36.852721],13);
    var osm  = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{
            attribution:'&copy;<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            maxZoom:25
    }).addTo(map);
    
    var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
	        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX,GeoEye,UPR-EGP',
          maxZoom:50,
    }).addTo(map);

    // ADD THE STREET NETWORK WMS LAYER,TRY TO USE WFS as GeoJSON instead
    var streetNetwork = L.tileLayer.wms("http://localhost:8080/geoserver/routing/wms",{
        layers:'routing:ways_noded',
        format:'image/png',
        transparent:true,
        attribution:'Street Network'
     }).addTo(map);

    //ADD A DRAGGABLE MARKER FOR SOURCE POINT
    var sourceMarker = L.marker([-1.307522,36.8561021],{
        draggable:true
    }).on("dragend",function(e){
        selectedPoint = e.target.getLatLng();
        getVertex(selectedPoint);
        getRoute();
    }).addTo(map);

    // ADD A DRAGGABLE MARKER FOR TARGET POINT
    var targetMarker = L.marker([ -1.2907,36.7885],{
        draggable:true
    }).on("dragend",function(e){
        selectedPoint = e.target.getLatLng();
        getVertex(selectedPoint);
        getRoute();
    }).addTo(map);
    
    // FUNCTION GETS THE NEAREST VERTEX
    function getVertex(selectedPoint){
        var vertexUrl = `${geoserverUrl}/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=routing:nearest_vertex
                         &maxFeatures=500000&viewparams=x:${selectedPoint.lng};y:${selectedPoint.lat};&outputFormat=application/json`;
        $.ajax({
            url:vertexUrl,
            async:false,
            success:function(data){
                loadVertex(data,selectedPoint.toString() === sourceMarker.getLatLng().toString());
            }
        });                         
    }

    // TO UPDATE THE SOURCE AND TARGET NODES AS RETURNED FROM GEOSERVER AND USE FOR A LATER QUERY
    function loadVertex(response,isSource){
        var features = response.features;
        map.removeLayer(pathLayer);
        if(isSource){
            source = features[0].properties.id;
        }
        else{
            target = features[0].properties.id;
        }
    }

    // FUNCTION TO GET THE SHORTEST PATH USING THE RETURNED VERTICES
    function getRoute(){
        var url = `${geoserverUrl}/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=routing:shortest_route&maxFeatures=500000
                    &viewparams=source:${source};target:${target}&outputFormat=application/json`;
        $.getJSON(url,function(data){
            map.removeLayer(pathLayer);
            pathLayer = L.geoJSON(data);
            map.addLayer(pathLayer);
        });            
    }
    getVertex(sourceMarker.getLatLng());
    getVertex(targetMarker.getLatLng());
    getRoute();
    
    L.control.mousePosition({
        position:'bottomright'
    }).addTo(map);
    
    // GROUP THE LAYERS
    var baseLayers,groupedOverlays;
    baseLayers = {
        "OSM":osm,
        "ESRI World Imagery":Esri_WorldImagery,
    } 
    groupedOverlays = {
        "Layers":{
            "Street Network":streetNetwork,
            //"Shortest Path":pathLayer
        }
    }  
    L.control.groupedLayers(baseLayers,groupedOverlays,{collapsed:true}).addTo(map);
}());

























