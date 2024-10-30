
/* Function Stack Size: 0x18 bytes */

void SERemoteMgr::parser:didEndElement:namespaceURI:qualifiedName:
               (ID this,SEL sel,ID parser,ID elementName,ID namespaceURI,ID qName)

{
  int iVar1;
  CLASS cls;
  char *propertyInfoString;
  undefined4 value;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  uint in_fpscr;
  double dVar6;
  double dVar7;
  undefined8 uVar8;
  char propType;
  
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_servertime);
  if (iVar1 == 0) {
    if (*(int *)(this + runningString) != 0) {
      value = _objc_msgSend(*(int *)(this + runningString),"intValue");
      dVar6 = (double)_objc_msgSend(*(undefined4 *)PTR__gTime_003582a0,"currentTime");
      dVar7 = (double)VectorSignedToFloat(value,(byte)(in_fpscr >> 0x15) & 3);
      gServerTimeOffset = VectorFloatToSigned(dVar6 - dVar7,3);
      if (gServerTimeOffset < 300) {
        gServerTimeOffset = 0;
      }
    }
LAB_0014fba0:
    _objc_msgSend(*(undefined4 *)(this + runningString),"release");
    *(undefined4 *)(this + runningString) = 0;
    return;
  }
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_dataversion);
  if (iVar1 == 0) {
    value = *(undefined4 *)(this + runningString);
    if (gDatabaseVersion == 0) {
      gDatabaseVersion = _objc_msgSend(value,"intValue");
      value = _objc_msgSend(&_OBJC_CLASS_$_NSUserDefaults,"standardUserDefaults");
      _objc_msgSend(value,"setInteger:forKey:",gDatabaseVersion,
                    *(undefined4 *)PTR__kServerDatabaseVersionKey_00358874);
    }
    else {
      iVar1 = _objc_msgSend(value,"intValue");
      if (gDatabaseVersion < iVar1) {
        _gDatabaseOutOfDate = 1;
        _objc_msgSend(parser,"abortParsing");
        _objc_msgSend(gpRemoteDelegate,"databaseRollback:",value);
      }
    }
    goto LAB_0014fba0;
  }
  value = _objc_msgSend(this,"theClass");
  value = _objc_msgSend(value,"acceptablePluralClasses");
  iVar1 = _objc_msgSend(value,"indexOfObject:",elementName);
  if (iVar1 != 0x7fffffff) {
    return;
  }
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_results);
  if (iVar1 == 0) {
    return;
  }
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_result);
  if (iVar1 == 0) {
finish_acceptable_plural_classes_and_return:
    uVar3 = *(undefined4 *)(this + currentObject);
    value = _objc_msgSend(&objc::class_t::SERemoteModel,"class");
    propType = _objc_msgSend(uVar3,"isKindOfClass:",value);
    if (propType != '\0') {
      _objc_msgSend(*(undefined4 *)(this + currentObject),"setUpdateTime:",
                    *(undefined4 *)(this + fetchDate));
    }
    _objc_msgSend(*(undefined4 *)(this + runningObjects),"addObject:",
                  *(undefined4 *)(this + currentObject));
    _objc_msgSend(*(undefined4 *)(this + currentObject),"release");
    *(undefined4 *)(this + currentObject) = 0;
    return;
  }
  value = _objc_msgSend(this,"theClass");
  value = _objc_msgSend(value,"acceptableClasses");
  iVar1 = _objc_msgSend(value,"indexOfObject:",elementName);
  if (iVar1 != 0x7fffffff) goto finish_acceptable_plural_classes_and_return;
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_property);
  if (iVar1 == 0) {
    uVar5 = *(undefined4 *)(this + currentObject);
    uVar4 = *(undefined4 *)(this + categoryID);
    uVar3 = *(undefined4 *)(this + propertyID);
    value = _objc_msgSend(*(undefined4 *)(this + runningString),"intValue");
    _objc_msgSend(uVar5,"setValueForCategoryID:propertyID:propertyValue:",uVar4,uVar3,value);
    _objc_msgSend(*(undefined4 *)(this + runningString),"release");
    *(undefined4 *)(this + runningString) = 0;
    return;
  }
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_loot);
  if (iVar1 == 0) {
    return;
  }
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_inventory);
  if (iVar1 == 0) {
    return;
  }
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_playdate);
  if (iVar1 == 0) {
    return;
  }
  iVar1 = _objc_msgSend(elementName,"caseInsensitiveCompare:",&cf_relationship);
  if (iVar1 == 0) {
    return;
  }
  if (*(int *)(this + currentObject) == 0) {
    return;
  }
  
  property = class_getProperty([currentObject class], [elementName UTF8String]);
  
  if (property == @nil) {
    return;
  }
  
  propertyInfoString = property_getAttributes(property);
  
  if (propertyInfoString == NULL) {
    return;
  }
  
  propType = propertyInfoString[1];
  
  if (propType == 'I' || propType == 'i') {
    value = [NSNumber numberWithInt: [runningString intValue]];
  }
  else {
    if (propType != '@') {
      goto setRunningStringToNilAndReturn;
    }
    
    value = [NSString stringWithUTF8String: propertyInfoString];
    value = [value componentsSeparatedByString: @"\""];
    value = [value objectAtIndex: 1];
    propType = [value isEqualToString: @"NSDate"];
    
    if (propType == '\0') {
      propType = [value isEqualToString: @"NSString"];
      
      if (propType != '\0') {
        [currentObject setValue: [runningString copy] forKey: elementName];
      }
      
      goto setRunningStringToNilAndReturn;
    }
    
    value = [NSDate dateWithTimeIntervalSince1970: [runningString doubleValue]];
  }
  
  [currentObject setValue: value forKey: elementName];
  
setRunningStringToNilAndReturn:
  runningString = @nil;
  return;
}

