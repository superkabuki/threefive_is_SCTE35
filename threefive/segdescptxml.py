    def _xmldeliveryrestrictions(self,node):
        setme = {
            "delivery_not_restricted_flag": False,
            "device_restrictions": table20[node.attrs["device_restrictions"]],
        }
        self.load(setme)
        self.load(node.attrs)

    @staticmethod
    def _xmlseg_upid(node):
        try:
            seg_upid = bytes.fromhex(node.value.lower().replace("0x", ""))
        except ERR:
            seg_upid = node.value
        return seg_upid
        
    def xmlupid(self,node):
        """
        upids parses out upids from a splice descriptors xml
        """
        seg_upid=self._xmlseg_upid(node)
        seg_upid_type = node.attrs["segmentation_upid_type"]
        self.segmentation_upid= seg_upid
        self.segmentation_upid_type=seg_upid_type,
        self.segmentation_upid_type_nameupid_map[seg_upid_type][0],
        self.segmentation_upid_length=len(seg_upid)

    def _xmlsegmentationdescriptor_child(self, child):
        """
        xmlsegmentationdescriptor_children parse the children
        of a SegmentationDescriptor.
        """
        if child.tag == "DeliveryRestrictions":
            self._xmldeliveryrestrictions(child)
        if child.tag == "SegmentationUpid":
            self.xmlupid(child)
    
    def _xmlsegmentation_message(self):
        if self.segmentation_type_id in table22:
            self.segmentation_message= table22[self.segmentation_type_id]
            
    def loadxml(self, node):
        """
        loadxml load segmentationdescriptor data from xml
        """
        self.load(node.attrs)
        self.segmentation_event_id_compliance_indicator=True
        self.program_segmentation_flag=True
        self.segmentation_duration_flag= False
        self.delivery_not_restricted_flag=True
        self.segmentation_event_id= hex(node.attrs["segmentation_event_id"])
        }
        self._xmlsegmentation_message()
        for child in node.children:
            self._xmlsegmentationdescriptor_child(child)





























