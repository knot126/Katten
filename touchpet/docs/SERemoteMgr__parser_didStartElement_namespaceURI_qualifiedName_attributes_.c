
/* Function Stack Size: 0x1c bytes */

void SERemoteMgr::parser:didStartElement:namespaceURI:qualifiedName:attributes:
               (ID this,SEL sel,ID parser,ID elementName,ID namespaceURI,ID qName,ID attributeDict)

{

  *(ID *)(this + currentElementName) = elementName;
  iVar6 = [elementName caseInsensitiveCompare: "dataversion"];
  if (iVar6 != NSOrderedSame) {
    uVar7 = [this theClass];
    uVar7 = [uVar7 acceptablePluralClasses];
    iVar6 = [uVar7 indexOfObject: elementName];
    
    // If elementName is an acceptable plural class of this class OR
    // elementName is equal to "results"
    if ((iVar6 != 0x7fffffff) ||
       ([elementName caseInsensitiveCompare: "results"] == NSOrderedSame)) {
      // Handle mega if this isnt "results"/a valid plural class (e.g. "pets")
      iVar6 = [elementName caseInsensitiveCompare: "mega"];
      if (iVar6 != NSOrderedSame) {
        return;
      }
      uVar7 = [attributeDict objectForKey: "count"];
      uVar7 = [uVar7 intValue];
      [SEMegaModel setTpdFriendRequestCount: uVar7];
      uVar7 = [attributeDict objectForKey: "totalcount"];
      uVar7 = [uVar7 intValue];
      [SEMegaModel setTpdFriendAvailableCount: uVar7];
      uVar7 = [attributeDict objectForKey: "pluscount"];
      uVar7 = [uVar7 intValue];
      [SEMegaModel setNontpdFriendRequestCount: uVar7];
      uVar7 = [attributeDict objectForKey: "followercount"];
      uVar7 = [uVar7 intValue];
      [SEMegaModel setNontpdFollowerRequestCount: uVar7];
      uVar7 = [attributeDict objectForKey: "totalpluscount"];
      uVar7 = [uVar7 intValue];
      [SEMegaModel setNontpdFriendAvailableCount: uVar7];
      uVar7 = [attributeDict objectForKey: "totalfollowercount"];
      uVar7 = [uVar7 intValue];
      [SEMegaModel setNontpdFollowersAvailableCount: uVar7];
      return;
    }
    
    iVar6 = [elementName caseInsensitiveCompare: "result"];
    // If elementName is not "result"
    if (iVar6 != NSOrderedSame) {
      uVar7 = [this theClass];
      uVar7 = [uVar7 acceptableClasses];
      iVar6 = [uVar7 indexOfObject: elementName];
      
      // If elementName is not an acceptable class name (e.g. this isnt a new
      // object of this type and is instead a property/relationship on the current
      // running object)
      if (iVar6 == 0x7fffffff) {
        // handle property
        iVar8 = [elementName caseInsensitiveCompare: "property"];
        iVar6 = categoryID;
        if (iVar8 == 0) {
          uVar7 = [attributeDict objectForKey: "category"];
          uVar7 = [uVar7 intValue];
          *(undefined4 *)(this + iVar6) = uVar7;
          iVar6 = propertyID;
          uVar7 = [attributeDict objectForKey: "id"];
          uVar7 = [uVar7 intValue];
          *(undefined4 *)(this + iVar6) = uVar7;
          createRunningString(this,(SEL)"createRunningString");
          return;
        }
        
        // handle relationship
        piVar9 = (int *)[elementName caseInsensitiveCompare: "relationship"];
        if (piVar9 == (int *)0x0) {
          uVar14 = *(undefined4 *)(this + currentObject);
          uVar7 = [SEPetModel class];
          cVar1 = [uVar14 isKindOfClass: uVar7];
          if (cVar1 == '\0') {
            return;
          }
          uVar7 = [SERelationshipModel alloc];
          uVar7 = [uVar7 init];
          uVar7 = [uVar7 autorelease];
          local_40 = piVar9;
          local_3c = piVar9;
          local_38 = piVar9;
          local_34 = piVar9;
          local_30 = piVar9;
          local_2c = piVar9;
          local_28 = piVar9;
          local_24 = piVar9;
          uVar14 = _objc_msgSend(attributeDict);
          uVar17 = 0x10;
          uVar10 = _objc_msgSend(uVar14,"countByEnumeratingWithState:objects:count:",&local_40,
                                 auStack_a0,0x10);
          if (uVar10 != 0) {
            iVar8 = *local_38;
            iVar6 = iVar8;
            while( true ) {
              uVar15 = 0;
              while( true ) {
                if (iVar8 != iVar6) {
                  [attributeDict allKeys];
                  _objc_enumerationMutation();
                }
                iVar6 = local_3c[uVar15];
                uVar15 = uVar15 + 1;
                uVar17 = [attributeDict objectForKey: iVar6];
                _objc_msgSend(uVar7,"setValue:forKey:",uVar17,iVar6);
                if (uVar10 <= uVar15) break;
                iVar6 = *local_38;
              }
              uVar17 = 0x10;
              uVar10 = _objc_msgSend(uVar14,"countByEnumeratingWithState:objects:count:",&local_40,
                                     auStack_a0,0x10);
              if (uVar10 == 0) break;
              iVar6 = *local_38;
            }
          }
          // check what this wants
          _objc_msgSend(*(undefined4 *)(this + currentObject),"addRelationship:",uVar7,currentObject
                        ,uVar17);
          return;
        }
        
        // handle playdate
        piVar9 = (int *)[elementName caseInsensitiveCompare: "playdate"];
        if (piVar9 == (int *)0x0) {
          uVar14 = *(undefined4 *)(this + currentObject);
          uVar7 = [SEPetModel class];
          cVar1 = [uVar14 isKindOfClass: uVar7];
          if (cVar1 == '\0') {
            return;
          }
          uVar7 = [SEPlaydateModel alloc];
          uVar7 = [uVar7 init];
          uVar7 = [uVar7 autorelease];
          local_60 = piVar9;
          local_5c = piVar9;
          local_58 = piVar9;
          local_54 = piVar9;
          local_50 = piVar9;
          local_4c = piVar9;
          local_48 = piVar9;
          local_44 = piVar9;
          uVar14 = _objc_msgSend(attributeDict);
          uVar17 = 0x10;
          uVar10 = _objc_msgSend(uVar14,"countByEnumeratingWithState:objects:count:",&local_60,
                                 auStack_e0,0x10);
          if (uVar10 != 0) {
            iVar8 = *local_58;
            iVar6 = iVar8;
            while( true ) {
              uVar15 = 0;
              while( true ) {
                if (iVar8 != iVar6) {
                  [attributeDict allKeys];
                  _objc_enumerationMutation();
                }
                iVar6 = local_5c[uVar15];
                uVar15 = uVar15 + 1;
                uVar17 = [attributeDict objectForKey: iVar6];
                [uVar7 setValue: uVar17 forKey: iVar6];
                if (uVar10 <= uVar15) break;
                iVar6 = *local_58;
              }
              uVar17 = 0x10;
              uVar10 = _objc_msgSend(uVar14,"countByEnumeratingWithState:objects:count:",&local_60,
                                     auStack_e0,0x10);
              if (uVar10 == 0) break;
              iVar6 = *local_58;
            }
          }
          _objc_msgSend(*(undefined4 *)(this + currentObject),"addPlaydate:",uVar7,currentObject,
                        uVar17);
          return;
        }
        
        iVar6 = [elementName caseInsensitiveCompare: "loot"];
        
        if (iVar6 != 0) {
          // handle inventory item
          iVar6 = [elementName caseInsensitiveCompare: "inventory"];
          if (iVar6 == 0) {
            uVar14 = *(undefined4 *)(this + currentObject);
            uVar7 = [SEPlayerModel class];
            cVar1 = [uVar14 isKindOfClass: uVar7];
            if (cVar1 == '\0') {
              return;
            }
            uVar16 = *(undefined4 *)(this + currentObject);
            uVar7 = [attributeDict objectForKey: "inventoryID"];
            uVar7 = [uVar7 intValue];
            uVar14 = [attributeDict objectForKey: "known"];
            cVar1 = [uVar14 boolValue];
            uVar14 = [attributeDict objectForKey: "rewarded"];
            cVar2 = [uVar14 boolValue];
            uVar14 = [attributeDict objectForKey: "owned"];
            cVar3 = [uVar14 boolValue];
            uVar14 = [attributeDict objectForKey: "gifted"];
            cVar4 = [uVar14 boolValue];
            uVar14 = [attributeDict objectForKey: "timeacquired"];
            uVar14 = [uVar14 intValue];
            uVar17 = [attributeDict objectForKey: "quantity"];
            uVar17 = [uVar17 intValue];
            uVar11 = [attributeDict objectForKey: "decaystate"];
            uVar11 = [uVar11 intValue];
            uVar12 = _objc_msgSend(attributeDict,"objectForKey:","fromdogID");
            iVar6 = [uVar12 length];
            if (iVar6 == 0) {
              local_100 = 0xffffffff;
            }
            else {
              local_100 = [uVar12 intValue];
            }
            uVar12 = [attributeDict objectForKey: "todogID"];
            iVar6 = [uVar12 length];
            if (iVar6 == 0) {
              local_fc = 0xffffffff;
            }
            else {
              local_fc = [uVar12 intValue];
            }
            uVar12 = [attributeDict objectForKey: "timegifted"];
            iVar6 = [uVar12 length];
            if (iVar6 == 0) {
              uVar12 = 0xffffffff;
            }
            else {
              uVar12 = [uVar12 intValue];
            }
            uVar13 = [attributeDict objectForKey: "isnew"];
            iVar6 = [uVar13 length];
            if (iVar6 == 0) {
              iVar6 = 0;
            }
            else {
              cVar5 = [uVar13 boolValue];
              iVar6 = (int)cVar5;
            }
            _objc_msgSend(uVar16,
                          "addInventoryItem:known:rewarded:owned:gifted:quantity:timeacquired:fromdo gID:todogID:timegifted:isnew:decaystate:"
                          ,uVar7,(int)cVar1,(int)cVar2,(int)cVar3,(int)cVar4,uVar17,uVar14,local_100
                          ,local_fc,uVar12,iVar6,uVar11);
            return;
          }
          goto LAB_0014f1b8;
        }
        
        // handle loot
        uVar14 = *(undefined4 *)(this + currentObject);
        uVar7 = [SEPlayerModel class];
        cVar1 = [uVar14 isKindOfClass: uVar7];
        if (cVar1 == '\0') {
          return;
        }
        uVar14 = *(undefined4 *)(this + currentObject);
        uVar7 = [SELootModel alloc];
        uVar7 = [uVar7 initWithXMLAttributeDict: attributeDict];
        iVar6 = [uVar7 hostPlayerID];
        iVar8 = [uVar14 playerID];
        if (iVar6 != iVar8) {
          iVar6 = [uVar7 lootPlayerID];
          iVar8 = [uVar14 playerID];
          if (iVar6 != iVar8) goto LAB_0014f694;
        }
        [uVar14 addLootModel: uVar7];
LAB_0014f694:
        [uVar7 release];
        return;
      }
    }
    
    // Initialise the current object
    uVar7 = [elementName capitalizedString];
    iVar8 = [SERemoteMgr classForTypeNamed: uVar7];
    if (iVar8 == 0) {
      iVar8 = [this theClass];
    }
    uVar7 = [iVar8 alloc];
    uVar7 = [uVar7 init];
    *(undefined4 *)(this + currentObject) = uVar7;
  }
LAB_0014f1b8:
  createRunningString(this,(SEL)"createRunningString");
  return;
}


