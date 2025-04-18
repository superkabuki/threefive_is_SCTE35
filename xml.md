# Xml
<pre>
    I pulled xml support a few months ago, I wasn't happy with the implementation. 
One out of every seven lines of code was xml specific, there was xml code everywhere.
It was all way too clunky. Everytime I touched one part of the code, something else would break.
 
 The xml parser worked completely different from the xml generator.
 Now, generating and parsing xml both use the Node class, it's much cleaner.
</pre>


# `Q.`Why would you write a xml parser for threefive3? 
 
# `A.`  __quadratic blowup__ and __billion laughs__. 

*  These are very old attacks, __over ten years old__,  and the [__python xml parsers are all vunerable__](https://docs.python.org/3/library/xml.html#xml-vulnerabilities) to both attacks.
 That's not good. That causes me a lot of concern. __If you know it's vumerable, don't document that it's broke, fix it__.
* __I'd fix the parsers__ for them, but __I've been banned from python's github repo__ for submitting patches to correct grammatical errors in PEPs, __criticizing PEP 668__ ( --break-system-packages), and trying to __start a mutiny__, but that's a story for another time.


 
* [Code stolen from here](https://gist.github.com/jordanpotti/04c54f7de46f2f0f0b4e6b8e5f5b01b0)
* 
![image](https://github.com/user-attachments/assets/121edabe-947f-47b9-a5ad-ed7b0b393474)



# Meet the new xml parser, Ultra Xml Parser Supreme.

This the fourth xml parser I've written, and the first one I actually like. 
The big difference is that when the xml data is parsed, it's marshaled into a threefive3.xml.Node instance.
My previous parsers took a lot of code in comparison to the size of threefive3. Parsing into a Node instance, 
allowed me to work in more general terms, each SCTE-35 object required a lot less specific code. Upids are good example. 
There used to be twenty Xml specific methods, about 120 lines, now there's four methods in 33 lines.

# Why do you care about any of this?
My point is that you shouldn't have to care, and you should expect code to not be vunerable to silly ass ten year old attacks. 

