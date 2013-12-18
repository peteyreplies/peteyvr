![Mammoth-interactive](images/mammoth.jpg)

* Start 
* Installing the template 
* CSS files 
* Changing the logo 
* Changing the header background image 
* Changing the Parallax background 
* Add/edit the carousel 
* Jquery plugins
* Adding social icons
* Credits



# Beachstrap Parallax one page HTML5 template

Documentation by "Mammoth Interactive"
Created: 31 October 2013  
Latest update 31 October 2013  

[www.mammoth-interactive.com](http://www.mammoth-interactive.com)

Thanks for purchasing this template and we hope you enjoy using it and creating something great. We'd love to see how you use this theme, so please send a link to your finished work to <info@mammoth-interactive.com>

## Installing the template
the basic structure of the HTML theme looks like the following:

	<!DOCTYPE html>
	<html lang="en">
	<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<meta charset="utf-8">
	<title>Beachstrap Theme</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<meta name="author" content="">
	<!-- STYLESHEETS -->
 	</head>
	<body>
 		<div id="content">	
				
		</div>
	<!-- JAVASCRIPTS -->
	</body>
	</html>
	
	
Everything goes inside the `<div>` named "content".

## CSS Files
The CSS theme file for Beachstrap is in the folder *css > beachstrap-style.css*
It follows the following structure:

	/* Table of Contents
	==================================================

	#GENERAL
	#HEADER
	#MAIN
	#CAROUSEL SECTION
	#PARALLAX SECTION
	#TEAM SECTION
	#SIGNUP SECTION
	#CONTACT SECTION
	#BLOG SECTION
	#FOOTER
	#MEDIA QUERIES

	==================================================
	*/


## Changing the logo
To the change the logo go through the following steps:

1. Create your new logo at 200px x 40px with a transparent background
2. Save your logo as **logo.png**
3. Place it in the folder *BeachStrap > images*

## Change the header background image
To change the background cover go through following steps:

1. Create your new background image at 1280px x 747px
2. Save it as **mainImage.jpg**
3. Place it in the folder *BeachStrap > images*

##Change the Parallax background image
To the change the parallax scrolling image, go through the following steps

1. Create a new image at 1280px x 500px and save it named **parallaxBg.jpg**
2. Drop it into the images folder: *BeachStrap > images*

#Add/edit the sliding carousel slides
The basic html for the carousel slide looks like the below.

To add a new slide, copy and paste this snippet and edit the contents between the `<div>...</div>` tags

```
	<!-- item -->
		<div class="item">
		<!-- edit contents here -->
			<div class="container">
				<h1>Example headline.</h1>
				<div class="caption">
				<p>Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi 				porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
				</div>
				</div>
				<img src="images/responsiveShot.png" alt="responsiveShot" class="img-responsive" >
				<p class="btn-wrp"><a class="c2a-button">Call to action</a></p>
		<!-- stop editing here -->
			</div>
	<!-- end item -->

``` 

**also you will need to add a new indicator to the carousel as you add new slides:**

```
	<!-- Indicators -->
	<ol class="carousel-indicators">
		<li data-target="#myCarousel" data-slide-to="0" class="active"></li>
		<li data-target="#myCarousel" data-slide-to="1"></li>
		<li data-target="#myCarousel" data-slide-to="2"></li>
	</ol>	
```    

Copy and paste the snippet below, under the last `<li>...</li>` tag to add a new indicator.

```
<li data-target="#myCarousel" data-slide-to="2"></li> 

```               

## Jquery plugins
Here is a list of all the Jquery plugins we have used:

    <script src="js/jquery.js"></script>
	<script src="js/waypoints.min.js"></script>
	<script src="js/beachstrap-script.js"></script>
	<script src="js/jquery.nav.js"></script>
	<script src="js/jquery.scrollTo.js"></script>

This template uses several javascript files, all of them are placed a folder called "js" and on googleapis servers. All javascript files are placed at the bottom of the page to speed up the loading time. If you want to add your google analytics code in the page, you should add it after the javascripts and before the `</body>` tag

##Adding social icons
Adding social icons of your choice is very easy. The theme uses Font Awesome icons. You can add your own with 

```
<i class="icon-twitter-sign icon-3x darkgray rm20 bm10"></i>

```
##Credits
Demo images (NOT included in the package)  
_http://www.flickr.com_

### Thanks to:

[**Danikapierce** ](http://www.flickr.com/photos/26629142@N03)  
www.flickr.com/photos/26629142@N03

[**Matito**](http://www.flickr.com/photos/riggott/)  
www.flickr.com/photos/riggott
 
[**Wesley Nitsckie** ](http://www.flickr.com/photos/nitsckie/)  
www.flickr.com/photos/nitsckie
  
[**Ed Kwon**](http://www.flickr.com/photos/kayone73/)  
www.flickr.com/photos/kayone73



