package me.vincentzyu.qwq.yolomirror.client;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.command.v2.ClientCommandRegistrationCallback;
import net.fabricmc.fabric.api.client.command.v2.FabricClientCommandSource;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.util.math.MatrixStack;
import net.minecraft.text.Text;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.FloatArgumentType;

public class YoloMirrorClient implements ClientModInitializer {

    private static float rollAngle = 0.0f;

    @Override
    public void onInitializeClient() {
        ClientCommandRegistrationCallback.EVENT.register(this::registerCommands);
    }

    private void registerCommands(CommandDispatcher<FabricClientCommandSource> dispatcher, net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.RegistrationEnvironment environment) {
        dispatcher.register(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal("roll")
                .then(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.argument("angle", FloatArgumentType.floatArg())
                        .executes(context -> {
                            float angle = FloatArgumentType.getFloat(context, "angle");
                            rollAngle = angle;
                            context.getSource().sendFeedback(Text.literal("Roll angle set to: " + angle));
                            return 1;
                        })));

        dispatcher.register(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal("roll_recover")
                .executes(context -> {
                    rollAngle = 0.0f;
                    context.getSource().sendFeedback(Text.literal("Roll angle recovered to 0"));
                    return 1;
                }));
    }

    public static float getRollAngle() {
        return rollAngle;
    }

    public static void setRollAngle(float angle) {
        rollAngle = angle;
    }
}
