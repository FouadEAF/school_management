// ignore_for_file: non_constant_identifier_names

import 'package:flutter/material.dart';
import 'package:toggle_switch/toggle_switch.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

Widget get switchMode {
  return ToggleSwitch(
    minWidth: 90.0,
    minHeight: 70.0,
    initialLabelIndex: 0,
    cornerRadius: 20.0,
    activeFgColor: Colors.white,
    inactiveBgColor: Colors.grey,
    inactiveFgColor: Colors.white,
    totalSwitches: 2,
    icons: const [
      FontAwesomeIcons.lightbulb,
      FontAwesomeIcons.solidLightbulb,
    ],
    iconSize: 30.0,
    activeBgColors: const [
      const [Colors.black45, Colors.black26],
      [Colors.yellow, Colors.orange]
    ],
    animate:
        true, // with just animate set to true, default curve = Curves.easeIn
    curve: Curves
        .bounceInOut, // animate must be set to true when using custom curve
    onToggle: (index) {
      print('switched to: $index');
    },
  );
}
