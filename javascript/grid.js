$(document).ready(function(){

    // get some info about the canvas for grayscale image
    var canvas_gray = document.getElementById('gray');
    var ctx_gray = canvas_gray.getContext('2d');
    function gray_canvas_size(imgObj) {
        target_width = 480;
        target_height = 480;

        target_ratio = target_width / target_height;
        real_ratio = imgObj.width / imgObj.height;
        if ( real_ratio > target_ratio ) {
            canvas_gray.width = target_width;
            canvas_gray.height = target_width / real_ratio;
            }
        else {
            canvas_gray.height = target_height;
            canvas_gray.width = target_height * real_ratio;
            }
        }
    function imageLoaded() {
        img.src = grayscaleImage(img);
        gray_canvas_size(img);
        console.log(canvas_gray.height, canvas_gray.width);
        ctx_gray.drawImage(img,0,0, canvas_gray.width, canvas_gray.height);
        }
    img = new Image();
    img.onload = imageLoaded;


    // get some info about the canvas for grid
    var pixel_1d = 12;
    var canvas_grid = document.getElementById('grid');
    var ctx_grid = canvas_grid.getContext('2d');
    var pixel_size = canvas_grid.width / pixel_1d;
    var w = pixel_1d;
    var h = pixel_1d;
    // create empty state array
    var state = new Array(w);
    for (var x = 0; x < w; ++x) {
        state[x] = new Array(h);
    }
    // Function to set a pixel
    function pixel(px, py, flag)
    {
        if (flag) {
            ctx_grid.fillStyle = 'black';
            state[px][py] = true;
        } else {
            ctx_grid.fillStyle = 'white';
            state[px][py] = false;
        }
        ctx_grid.fillRect(px * pixel_size, py * pixel_size, pixel_size, pixel_size);
    }

    // click event, using jQuery for cross-browser convenience
    $(canvas_grid).click(function(e) {
        // get mouse click position
        var mx = e.offsetX;
        var my = e.offsetY;

        // calculate grid square numbers
        var gx = ~~ (mx / pixel_size);
        var gy = ~~ (my / pixel_size);
    
        // make sure we're in bounds
        if (gx < 0 || gx >= w || gy < 0 || gy >= h) {
            return;
        }

        if (state[gx][gy]) {
            pixel(gx, gy, false);
        } else {
            pixel(gx, gy, true);
        }
    });

    // Adapted from http://www.ajaxblender.com/article-sources/jquery/convert-image-grayscale/index.html
    function grayscaleImage(imgObj){
        // Make the canvas in bigger for now..
        canvas_gray.width = imgObj.width;
        canvas_gray.height = imgObj.height;        
        ctx_gray.drawImage(imgObj, 0, 0);
        var imgPixels = ctx_gray.getImageData(0, 0, canvas_gray.width, canvas_gray.height);
        for(var x = 0; x < imgPixels.width; x++){
            for(var y = 0; y < imgPixels.height; y++){
                var i = (y * 4) * imgPixels.width + x * 4;
                var avg = (imgPixels.data[i] + imgPixels.data[i + 1] + imgPixels.data[i + 2]) / 3;
                  if (avg > 127) {
                      imgPixels.data[i] = 255;
                      imgPixels.data[i + 1] = 255;
                      imgPixels.data[i + 2] = 255;
                  }
                  else {
                      imgPixels.data[i] = 0;
                      imgPixels.data[i + 1] = 0;
                      imgPixels.data[i + 2] = 0;
                  }
            }
        }
        
        // Write the image to the canvas, so we can use the monochrome
        ctx_gray.putImageData(imgPixels, 0, 0, 0, 0, imgPixels.width, imgPixels.height);

        // Leabing Javascript - but ~~ was key
        var x_space = ~~  (canvas_gray.width / pixel_1d);
        var y_space = ~~  (canvas_gray.height / pixel_1d);
        var blob_pixels = (x_space*y_space)/2; //Divide by two - more than half black
        for(var x = 0; x < pixel_1d; x++){
            for(var y = 0; y < pixel_1d; y++){
                mono = 0;
                for(var px = (x*x_space); px < ((x+1)*x_space); px++){
                    for(var py = (y*y_space); py < ((y+1)*y_space); py++){
                        var i = (py * 4) * imgPixels.width + px * 4;
                        if (imgPixels.data[i] > 127) {
                            mono++;
                        }
                    }
                }
                if (mono<blob_pixels) {
                    pixel(x, y, true);
                } else {
                    pixel(x, y, false);

                }
            }
        }
        // Pass back the data
        return canvas_gray.toDataURL();
    }
    

    // Adapted from http://stackoverflow.com/questions/13938686/can-i-load-a-local-file-into-an-html-canvas-element
    function loadImage() {
        var input, file, fr;
        if (typeof window.FileReader !== 'function') {
            console.log("The file API isn't supported on this browser yet.");
            return;
        }
        input = document.getElementById('imgfile');
        if (!input) {
            console.log("Um, couldn't find the imgfile element.");
        }
        else if (!input.files) {
            console.log("This browser doesn't seem to support the `files` property of file inputs.");
        }
        else if (!input.files[0]) {
            console.log("Please select a file before clicking 'Load'");
        }
        else {
            file = input.files[0];
            fr = new FileReader();
            fr.onload = createImage;
            fr.readAsDataURL(file);
        }
        function createImage() {
//            img = new Image();
//            img.onload = imageLoaded;
            img.src = fr.result;
        }
    }

    // Link loadImage to button
    $('#loadImage').click(function(){
        loadImage(); 
    });

    $('#btn').click(function() {
        alert("Hello");
    });

    $('#toastIt').click(function(e) {
        e.preventDefault();
        $('#toastItForm').attr('action', "/test1").submit();
    });


    // Set Default Logo
    // convert -pointsize 356  label:'PT' -fill black -pointsize 48 -gravity SouthWest label:'-- Pixelate Toast --' -composite logo.png
    img.src = './logo.png';


});


