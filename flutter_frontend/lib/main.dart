import 'package:flutter/material.dart';
import 'package:flutter_frontend/constants.dart';
import 'package:flutter_frontend/web/knowledge_manager_page.dart';
import 'package:flutter_frontend/web/web_home_page.dart';
import 'package:get/get_connect/http/src/utils/utils.dart';
import 'package:get/get_navigation/get_navigation.dart';
import 'package:get/get_navigation/src/root/get_material_app.dart';
import 'dart:io'; // To check platform

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      theme: ThemeData(
        primaryColor: AppColor.primary,
        scaffoldBackgroundColor: AppColor.primary,
      ),
      debugShowCheckedModeBanner: false,
      initialRoute: getDefaultRoute(),
      title: 'Smart Search',
      getPages: [
        GetPage(name: WebHomePage.WEB_HOME_PAGE_ROUTE, page: () => WebHomePage()),
        GetPage(name: KnowledgeManager.WEB_KOWLEDGE_MANAGER_ROUTE, page: () => KnowledgeManager())
      ],
    );
  }

    String getDefaultRoute() {
      return WebHomePage.WEB_HOME_PAGE_ROUTE;
    /*if (Platform.isAndroid) {
      return '/android';
    } else if (Platform.isIOS) {
      return '/ios';
    } else if (Platform.isMacOS || Platform.isWindows || Platform.isLinux) {
      return '/desktop';
    } else {
      return '/web'; // For Web
    }*/
  }

}
