/* Function Stack Size: 0x18 bytes */

void SERemoteMgr::parser:didEndElement:namespaceURI:qualifiedName:
               (ID this,SEL sel,ID parser,ID elementName,ID namespaceURI,ID qName)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  uint in_fpscr;
  double dVar7;
  double dVar8;
  undefined8 uVar9;
  
  iVar2 = [elementName caseInsensitiveCompare: "servertime"];
  if (iVar2 == 0) {
    if (*(int *)(this + runningString) != 0) {
      uVar3 = _objc_msgSend(*(int *)(this + runningString),"intValue");
      dVar7 = (double)_objc_msgSend(*(undefined4 *)PTR__gTime_003582a0,"currentTime");
      dVar8 = (double)VectorSignedToFloat(uVar3,(byte)(in_fpscr >> 0x15) & 3);
      gServerTimeOffset = VectorFloatToSigned(dVar7 - dVar8,3);
      if (gServerTimeOffset < 300) {
        gServerTimeOffset = 0;
      }
    }
LAB_0014fba0:
    _objc_msgSend(*(undefined4 *)(this + runningString),"release");
    *(undefined4 *)(this + runningString) = 0;
    return;
  }
  iVar2 = [elementName caseInsensitiveCompare: "dataversion"];
  if (iVar2 == 0) {
    uVar3 = *(undefined4 *)(this + runningString);
    if (gDatabaseVersion == 0) {
      gDatabaseVersion = [uVar3 intValue];
      uVar3 = _objc_msgSend(&_OBJC_CLASS_$_NSUserDefaults,"standardUserDefaults");
      _objc_msgSend(uVar3,"setInteger:forKey:",gDatabaseVersion,
                    *(undefined4 *)PTR__kServerDatabaseVersionKey_00358874);
    }
    else {
      iVar2 = [uVar3 intValue];
      if (gDatabaseVersion < iVar2) {
        _gDatabaseOutOfDate = 1;
        [parser abortParsing];
        [gpRemoteDelegate databaseRollback: uVar3];
      }
    }
    goto LAB_0014fba0;
  }
  
  // if the element name is "results" or an acceptable plural class of anything
  // then ignore it
  uVar3 = [this theClass];
  uVar3 = [uVar3 acceptablePluralClasses];
  iVar2 = [uVar3 indexOfObject: elementName];
  if (iVar2 != 0x7fffffff) {
    return;
  }
  iVar2 = [elementName caseInsensitiveCompare: "results"];
  if (iVar2 == 0) {
    return;
  }
  iVar2 = [elementName caseInsensitiveCompare: "result"];
  if (iVar2 == 0) {
LAB_0014fd34:
    uVar4 = *(undefined4 *)(this + currentObject);
    uVar3 = [SERemoteModel class];
    cVar1 = [uVar4 isKindOfClass: uVar3];
    if (cVar1 != '\0') {
      _objc_msgSend(*(undefined4 *)(this + currentObject),"setUpdateTime:",
                    *(undefined4 *)(this + fetchDate));
    }
    _objc_msgSend(*(undefined4 *)(this + runningObjects),"addObject:",
                  *(undefined4 *)(this + currentObject));
    _objc_msgSend(*(undefined4 *)(this + currentObject),"release");
    *(undefined4 *)(this + currentObject) = 0;
    return;
  }
  uVar3 = [this theClass];
  uVar3 = [uVar3 acceptableClasses];
  iVar2 = [uVar3 indexOfObject: elementName];
  if (iVar2 != 0x7fffffff) goto LAB_0014fd34;
  iVar2 = [elementName caseInsensitiveCompare: "property"];
  if (iVar2 == 0) {
    uVar6 = *(undefined4 *)(this + currentObject);
    uVar5 = *(undefined4 *)(this + categoryID);
    uVar4 = *(undefined4 *)(this + propertyID);
    uVar3 = _objc_msgSend(*(undefined4 *)(this + runningString),"intValue");
    _objc_msgSend(uVar6,"setValueForCategoryID:propertyID:propertyValue:",uVar5,uVar4,uVar3);
    _objc_msgSend(*(undefined4 *)(this + runningString),"release");
    *(undefined4 *)(this + runningString) = 0;
    return;
  }
  iVar2 = [elementName caseInsensitiveCompare: "loot"];
  if (iVar2 == 0) {
    return;
  }
  iVar2 = [elementName caseInsensitiveCompare: "inventory"];
  if (iVar2 == 0) {
    return;
  }
  iVar2 = [elementName caseInsensitiveCompare: "playdate"];
  if (iVar2 == 0) {
    return;
  }
  iVar2 = [elementName caseInsensitiveCompare: "relationship"];
  if (iVar2 == 0) {
    return;
  }
  if (*(int *)(this + currentObject) == 0) {
    return;
  }
  uVar3 = _objc_msgSend(*(int *)(this + currentObject),"class");
  uVar4 = [elementName UTF8String];
  iVar2 = _class_getProperty(uVar3,uVar4);
  if (iVar2 == 0) {
    return;
  }
  iVar2 = _property_getAttributes();
  if (iVar2 == 0) {
    return;
  }
  cVar1 = *(char *)(iVar2 + 1);
  if (cVar1 == 'I' || cVar1 == 'i') {
    uVar3 = _objc_msgSend(*(undefined4 *)(this + runningString),"intValue");
    uVar3 = _objc_msgSend(&_OBJC_CLASS_$_NSNumber,"numberWithInt:",uVar3);
  }
  else {
    if (cVar1 != '@') goto LAB_0014ff4c;
    uVar3 = _objc_msgSend(&_OBJC_CLASS_$_NSString,"stringWithUTF8String:");
    uVar3 = _objc_msgSend(uVar3,"componentsSeparatedByString:",&cf_");
    uVar3 = [uVar3 objectAtIndex: 1];
    cVar1 = [uVar3 isEqualToString: "NSDate"];
    if (cVar1 == '\0') {
      cVar1 = [uVar3 isEqualToString: "NSString"];
      if (cVar1 != '\0') {
        uVar3 = _objc_msgSend(*(undefined4 *)(this + runningString),"copy");
        _objc_msgSend(*(undefined4 *)(this + currentObject),"setValue:forKey:",uVar3,elementName);
        [uVar3 release];
      }
      goto LAB_0014ff4c;
    }
    uVar9 = _objc_msgSend(*(undefined4 *)(this + runningString),"doubleValue");
    uVar3 = _objc_msgSend(&_OBJC_CLASS_$_NSDate,"dateWithTimeIntervalSince1970:",(int)uVar9,
                          (int)((ulonglong)uVar9 >> 0x20));
  }
  _objc_msgSend(*(undefined4 *)(this + currentObject),"setValue:forKey:",uVar3,elementName);
LAB_0014ff4c:
  _objc_msgSend(*(undefined4 *)(this + runningString),"release");
  *(undefined4 *)(this + runningString) = 0;
  return;
}
