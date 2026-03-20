package me.vincentzyu.qwq.yolomirror.mixin.client;

import me.vincentzyu.qwq.yolomirror.client.YoloMirrorClient;
import net.minecraft.client.render.GameRenderer;
import net.minecraft.client.util.math.MatrixStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(GameRenderer.class)
public class GameRendererMixin {

    @Inject(method = "render", at = @At(value = "INVOKE", target = "net/minecraft/client/render/GameRenderer.renderWorld(FJLnet/minecraft/client/util/math/MatrixStack;)V"))
    private void injectRoll(float tickDelta, long startTime, boolean tick, CallbackInfo ci) {
        MatrixStack matrixStack = new MatrixStack();
        float rollAngle = YoloMirrorClient.getRollAngle();
        if (rollAngle != 0.0f) {
            matrixStack.multiply(org.joml.Quaternionf.rotateZ((float) Math.toRadians(rollAngle)));
        }
    }

    @Inject(method = "renderWorld", at = @At(value = "HEAD"))
    private void injectRollInRenderWorld(float tickDelta, long limitTime, MatrixStack matrices, CallbackInfo ci) {
        float rollAngle = YoloMirrorClient.getRollAngle();
        if (rollAngle != 0.0f) {
            matrices.multiply(org.joml.Quaternionf.rotateZ((float) Math.toRadians(rollAngle)));
        }
    }
}
