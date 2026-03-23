package me.vincentzyu.qwq.yolomirror.mixin.client;

import com.llamalad7.mixinextras.injector.ModifyExpressionValue;
import me.vincentzyu.qwq.yolomirror.client.YoloMirrorClient;
import net.minecraft.client.render.GameRenderer;
import org.joml.Matrix4f;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;

/**
 * 在 1.21.x (MC >= 1.21.0) 中，renderWorld 的签名已改为 renderWorld(RenderTickCounter)，
 * 不再直接暴露 MatrixStack。相机朝向矩阵通过 Matrix4f.rotation(Quaternionfc) 设置。
 * 使用 MixinExtras 的 @ModifyExpressionValue 拦截该调用并追加 Z 轴 roll 旋转。
 */
@Mixin(GameRenderer.class)
public class GameRendererMixin {

    @ModifyExpressionValue(
            method = "renderWorld",
            at = @At(value = "INVOKE", target = "Lorg/joml/Matrix4f;rotation(Lorg/joml/Quaternionfc;)Lorg/joml/Matrix4f;")
    )
    private Matrix4f applyRoll(Matrix4f matrix) {
        float rollAngle = YoloMirrorClient.getRollAngle();
        if (rollAngle != 0.0f) {
            matrix.rotateLocal((float) Math.toRadians(rollAngle), 0f, 0f, 1f);
        }
        return matrix;
    }
}
