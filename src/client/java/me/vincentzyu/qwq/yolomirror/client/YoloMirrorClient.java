package me.vincentzyu.qwq.yolomirror.client;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.command.v2.ClientCommandRegistrationCallback;
import net.fabricmc.fabric.api.client.command.v2.FabricClientCommandSource;
import net.minecraft.text.Text;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.FloatArgumentType;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.net.URI;
import java.net.URISyntaxException;

public class YoloMirrorClient implements ClientModInitializer {

    private static float rollAngle = 0.0f;
    private static float targetRollAngle = 0.0f;
    private static WebSocketClient webSocketClient;
    private static boolean isWebSocketConnected = false;
    private static final float SMOOTHING_FACTOR = 0.1f;

    @Override
    public void onInitializeClient() {
        ClientCommandRegistrationCallback.EVENT.register(this::registerCommands);
        // Start a thread to handle smooth angle transitions
        new Thread(() -> {
            while (true) {
                if (rollAngle != targetRollAngle) {
                    rollAngle += (targetRollAngle - rollAngle) * SMOOTHING_FACTOR;
                    // If the difference is very small, set them equal to avoid oscillation
                    if (Math.abs(targetRollAngle - rollAngle) < 0.01f) {
                        rollAngle = targetRollAngle;
                    }
                }
                try {
                    Thread.sleep(16); // ~60 FPS
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    private void registerCommands(CommandDispatcher<FabricClientCommandSource> dispatcher, net.minecraft.command.CommandRegistryAccess registryAccess) {
        dispatcher.register(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal("roll")
                .then(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.argument("angle", FloatArgumentType.floatArg())
                        .executes(context -> {
                            float angle = FloatArgumentType.getFloat(context, "angle");
                            targetRollAngle = angle;
                            context.getSource().sendFeedback(Text.literal("Roll angle set to: " + angle));
                            return 1;
                        })));

        dispatcher.register(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal("roll_recover")
                .executes(context -> {
                    targetRollAngle = 0.0f;
                    context.getSource().sendFeedback(Text.literal("Roll angle recovered to 0"));
                    return 1;
                }));

        dispatcher.register(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal("start_roll_mirror")
                .executes(context -> {
                    startWebSocketConnection();
                    context.getSource().sendFeedback(Text.literal("Starting roll mirror connection..."));
                    return 1;
                }));

        dispatcher.register(net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal("end_roll_mirror")
                .executes(context -> {
                    stopWebSocketConnection();
                    context.getSource().sendFeedback(Text.literal("Stopping roll mirror connection..."));
                    return 1;
                }));
    }

    private void startWebSocketConnection() {
        try {
            URI uri = new URI("ws://0.0.0.0:60321");
            webSocketClient = new WebSocketClient(uri) {
                @Override
                public void onOpen(ServerHandshake handshakedata) {
                    isWebSocketConnected = true;
                    System.out.println("WebSocket connected!");
                }

                @Override
                public void onMessage(String message) {
                    try {
                        JsonObject json = JsonParser.parseString(message).getAsJsonObject();
                        if (json.has("type") && json.get("type").getAsString().equals("roll_control")) {
                            if (json.has("angle")) {
                                float angle = json.get("angle").getAsFloat();
                                targetRollAngle = angle;
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onClose(int code, String reason, boolean remote) {
                    isWebSocketConnected = false;
                    System.out.println("WebSocket disconnected!");
                }

                @Override
                public void onError(Exception ex) {
                    isWebSocketConnected = false;
                    ex.printStackTrace();
                }
            };
            webSocketClient.connect();
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
    }

    private void stopWebSocketConnection() {
        if (webSocketClient != null && webSocketClient.isOpen()) {
            webSocketClient.close();
        }
        isWebSocketConnected = false;
    }

    public static float getRollAngle() {
        return rollAngle;
    }

    public static void setRollAngle(float angle) {
        targetRollAngle = angle;
    }
}
