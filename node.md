# The Node Class 
#### _Coming in threefive3 v3.0.45_
If you parse xml into a threefive3 object, the xml is first parsed into a Node instance.<br>
If you return xml from a threefive3 object, A Node instance is returned.

## Here's what you can do with a Node instance.

* __Parse a DASH mpd__
* use __Ultra Xml Parser Supreme__ (_uxps_)
```py3

a@fu:~/threefive3$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u3, Dec 30 2024, 22:36:23)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive3 import reader
>>>> from threefive3.uxp import uxps
>>>> data = reader('/home/a/fu.mpd').read().strip().decode()
>>>> n= uxps(data)         # use uxps (Ultra Xml Parser Supreme) to parse into a Node instance (n)
```
* __search recursively for Event tags in the MPD xml__
* __Node.findtag(tag)__ returns a NodeList instance, so you can modify the Xml if needed.
 ```py3
>>>> events = n.findtag("Event")
>>>> events
[         <Event presentationTime="1725946427520" duration="0.426667" id="14268737">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blBf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946548480" duration="0.426667" id="14268738">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blCf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946669440" duration="0.426667" id="14268739">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blDf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946790400" duration="0.426667" id="14268740">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blEf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946911360" duration="0.426667" id="14268741">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blFf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725947032320" duration="0.426667" id="14268742">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blGf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
]
```
* __These events can be modified or deleted and the changes applied in real time.__
```py3
>>>> events  = n.findtag("Event")
>>>> len(events)
6
>>>> events.pop()
>>>> len(events)
5
>>>> events.pop(0)
>>>> len(events)
4
>>>> 
```
* you can also search with __Node.findattr(attr)__ for xml nodes that have an attribute
```py3
>>>> bwidth_nodes=n.findattr("bandwidth")
>>>> bwidth_nodes
[<Representation   id="audio_eng" bandwidth="128000"/>
, <Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```
* __you can modify those nodes too.__
* Here I add an attribute to the first bwidth_node
```py3
>>>> bwidth_nodes[0].addattr("fu","2you")
>>>> bwidth_nodes
[<Representation   id="audio_eng" bandwidth="128000" fu="2you"/>
, <Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```
* __access the parent__
* _You can also chain parents like bwidth_nodes[0].parent.parent_
```py3
>>>> bwidth_nodes[0].parent    

<AdaptationSet   id="1" group="1" contentType="audio" lang="en" segmentAlignment="true" audioSamplingRate="48000" mimeType="audio/mp4" codecs="mp4a.40.2" startWithSAP="1">
   <AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="1"/>
   <Role schemeIdUri="urn:mpeg:dash:role:2011" value="main"/>
   <SegmentTemplate timescale="48000" startNumber="898930439" initialization="scte35-$RepresentationID$.dash" media="scte35-$RepresentationID$-$Time$.dash">
      <SegmentTimeline>
         <S t="82845429166080" d="92160" r="311"/>
      </SegmentTimeline>
   </SegmentTemplate>
   <Representation id="audio_eng" bandwidth="128000" fu="2you"/>
</AdaptationSet>
````
* __go crazy with namespaces__
    * namespaces can be set from the top, or by node.
    *  namespaces can set on tags and/or attributes.
<br><br>

* set the namespace on the first node
```py3
>>>> bwidth_nodes[0].namespace.ns="supercool"
>>>> bwidth_nodes
[   <supercool:Representation id="audio_eng" bandwidth="128000" fu="2you"/>
, <Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```
* set the second node to a different namespace
```py3
>>>> bwidth_nodes[1].namespace.ns="hottamale"
>>>> bwidth_nodes
[   <supercool:Representation id="audio_eng" bandwidth="128000" fu="2you"/>
, <hottamale:Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```
* apply the namespace to the attributes the second node
```py3
>>>> bwidth_nodes[1].namespace.all = True
>>>> bwidth_nodes
[   <supercool:Representation id="audio_eng" bandwidth="128000" fu="2you"/>
, <hottamale:Representation   hottamale:id="video" hottamale:bandwidth="1000000" hottamale:ScanType="progressive"/>
]
```

### Help is built-in
```py3
Help on class Node in module threefive3.xml:

class Node(builtins.object)
 |  Node(tag, value='', attrs=None, ns=None)
 |  
 |  The Node class is to create an xml node.
 |  
 |  An instance of Node has:
 |  
 |      tag :      <tag> </tag>
 |      value  :    <tag>value</tag>
 |      attrs :     <tag attrs[k]="attrs[v]">
 |      children :  <tag><children[0]></children[0]</tag>
 |      depth:      tab depth for printing (automatically set)
 |      namespace:    a NameSpace instance for the Node
 |  
 |  Use like this:
 |  
 |      from threefive3.xml import Node
 |  
 |      ts = Node('TimeSignal')
 |      st = Node('SpliceTime',attrs={'pts_time':3442857000})
 |      ts.addchild(st)
 |      print(ts)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, tag, value='', attrs=None, ns=None)
 |  
 |  __repr__(self)
 |  
 |  addattr(self, attr, value)
 |      addattr add an attribute
 |  
 |  addchild(self, child, slot=None)
 |      addchild adds a child node
 |      set slot to insert at index slot.
 |  
 |  addcomment(self, comment, slot=None)
 |      addcomment add a Comment node
 |  
 |  children_namespaces(self)
 |      children_namespaces give children your namespace
 |  
 |  chk_obj(self, obj)
 |      chk_obj determines if
 |      obj is self, or another obj
 |      for self.set_ns and self.mk
 |  
 |  drop(self, obj=None)
 |      drop delete self
 |  
 |  dropattr(self, attr)
 |      dropattr remove an attribute
 |  
 |  dropchild(self, child)
 |      dropchild remove a child
 |      
 |      example:
 |      a_node.dropchild(a_node.children[3])
 |  
 |  findattr(self, attr, obj=None)
 |      findattr  recursively searches children for all nodes that
 |      have an attribute that matches attr. findattr returns a NodeList.
 |  
 |  findtag(self, tag, obj=None)
 |      findtag  recursively searches children for
 |      all nodes with a tag that matches tag.
 |      findtag returns a NodeList.
 |  
 |  get_indent(self)
 |      get_indent returns a string of spaces the required depth for a node
 |  
 |  mk(self, obj=None)
 |      mk make the Node as xml.
 |  
 |  mk_ans(self, attrs)
 |      mk_ans set namespace on attributes
 |  
 |  mk_tag(self)
 |      mk_tag add namespace to node name
 |  
 |  rendr_all(self, ndent, tag)
 |      rendr_all renders the Node instance and it's children in xml.
 |  
 |  rendr_attrs(self, ndent, tag)
 |      rendrd_attrs renders xml attributes
 |  
 |  set_depth(self)
 |      set_depth is used to format
 |      tabs in output
 |  
 |  set_ns(self, ns=None)
 |      set_ns set namespace on the Node
 |  
 |  set_parent(self, obj=None)
 |      set_parent set the parent node of this node.
 |      a top level node's parent will be None.
 |  
```


