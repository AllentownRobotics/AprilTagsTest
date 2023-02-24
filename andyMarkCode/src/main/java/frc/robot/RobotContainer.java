package frc.robot;

import frc.robot.Constants;
import frc.robot.commands.DriveCMD;
import frc.robot.commands.MoveToTag;
import frc.robot.commands.PointToTag;
import frc.robot.subsystems.DriveTrain;
import frc.robot.subsystems.VisionSub;

import java.util.function.BooleanSupplier;

import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.button.CommandXboxController;
import edu.wpi.first.wpilibj2.command.button.JoystickButton;
import edu.wpi.first.wpilibj2.command.button.Trigger;

public class RobotContainer {
  
  public static DriveTrain drivetrainsubsystem;
  public static VisionSub visionSubsystem;
  public static XboxController controller;

  public RobotContainer() {
    controller = new XboxController(Constants.kDriverControllerPort);
    drivetrainsubsystem = new DriveTrain();
    visionSubsystem = new VisionSub();
    drivetrainsubsystem.setDefaultCommand(new DriveCMD());
    configureBindings();
  }


  private void configureBindings() {
    new JoystickButton(controller, XboxController.Button.kRightBumper.value).whileTrue(new PointToTag());
    //new JoystickButton(controller, XboxController.Button.kLeftBumper.value).whileTrue(new MoveToTag());

  }



}
